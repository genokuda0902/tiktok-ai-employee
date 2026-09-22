"""PostgreSQL-backed job ledger. No production activation or external delivery.

Requires psycopg>=3 and an externally provisioned DATABASE_URL. Never log DSN.
Every state transition is fenced by lease token. Expired claims require operator
reconciliation of deterministic artifact key before a new render is allowed.
"""
import hashlib
import uuid
from datetime import datetime, timezone

DDL = """
CREATE TABLE IF NOT EXISTS automation_jobs (
 job_id text PRIMARY KEY, plan_id text NOT NULL, account_id text NOT NULL,
 scheduled_at timestamptz NOT NULL, status text NOT NULL DEFAULT 'queued',
 attempts integer NOT NULL DEFAULT 0, lease_token uuid, lease_until timestamptz,
 artifact_key text NOT NULL UNIQUE, artifact_uri text, artifact_sha256 text,
 qa_result jsonb, error_code text, handoff_status text NOT NULL DEFAULT 'blocked',
 updated_at timestamptz NOT NULL DEFAULT now(),
 CHECK (status IN ('queued','rendering','reconcile_required','qa_pending','qa_rejected','human_review','ready','failed')),
 CHECK (handoff_status IN ('blocked','ready','delivered'))
);
"""


def deterministic_id(account_id, day, slot):
    if slot not in (1, 2):
        raise ValueError('slot must be 1 or 2')
    return hashlib.sha256(f'{account_id}|{day}|{slot}'.encode()).hexdigest()


class Ledger:
    """Pass an already authenticated psycopg connection; caller owns lifecycle."""
    def __init__(self, connection):
        self.conn = connection

    def initialize(self):
        with self.conn.transaction():
            self.conn.execute(DDL)

    def submit(self, job_id, plan_id, account_id, scheduled_at):
        if not all((job_id, plan_id, account_id)) or scheduled_at.tzinfo is None:
            raise ValueError('missing identity or timezone')
        key = f'jobs/{job_id}/original.mp4'
        with self.conn.transaction():
            row = self.conn.execute('''INSERT INTO automation_jobs
                (job_id,plan_id,account_id,scheduled_at,artifact_key)
                VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING RETURNING job_id''',
                (job_id,plan_id,account_id,scheduled_at,key)).fetchone()
        return 'queued' if row else 'duplicate'

    def claim(self, job_id, *, max_attempts=3, lease_seconds=900):
        """Atomic claim. An expired render is NOT retried without reconciliation."""
        token = uuid.uuid4()
        with self.conn.transaction():
            row = self.conn.execute('''UPDATE automation_jobs SET
                status='rendering', attempts=attempts+1, lease_token=%s,
                lease_until=now()+(%s * interval '1 second'),updated_at=now()
                WHERE job_id=%s AND status='queued' AND attempts < %s
                RETURNING artifact_key''', (token,lease_seconds,job_id,max_attempts)).fetchone()
        return {'token':str(token),'artifact_key':row[0]} if row else None

    def heartbeat(self, job_id, token, lease_seconds=900):
        with self.conn.transaction():
            row=self.conn.execute('''UPDATE automation_jobs SET
                lease_until=now()+(%s * interval '1 second'),updated_at=now()
                WHERE job_id=%s AND lease_token=%s AND status='rendering'
                AND lease_until>now() RETURNING job_id''',
                (lease_seconds,job_id,token)).fetchone()
        return bool(row)

    def rendered(self, job_id, token, uri, sha256):
        if not uri or len(sha256)!=64:
            raise ValueError('verified artifact URI and sha256 required')
        with self.conn.transaction():
            row=self.conn.execute('''UPDATE automation_jobs SET status='qa_pending',
                artifact_uri=%s,artifact_sha256=%s,lease_token=NULL,lease_until=NULL,
                updated_at=now() WHERE job_id=%s AND lease_token=%s
                AND status='rendering' AND lease_until>now() RETURNING job_id''',
                (uri,sha256,job_id,token)).fetchone()
        return bool(row)

    def expire(self):
        """Mark uncertain external side effects; never automatically render again."""
        with self.conn.transaction():
            rows=self.conn.execute('''UPDATE automation_jobs SET status='reconcile_required',
                lease_token=NULL,lease_until=NULL,error_code='lease_expired',updated_at=now()
                WHERE status='rendering' AND lease_until<=now() RETURNING job_id''').fetchall()
        return [row[0] for row in rows]

    def qa(self, job_id, passed, report_json):
        """Only a real QA report can advance; human approval remains separate."""
        if not isinstance(report_json, dict) or report_json.get('mock') is True:
            raise ValueError('real QA report required')
        import json
        status='human_review' if passed is True else 'qa_rejected'
        with self.conn.transaction():
            row=self.conn.execute('''UPDATE automation_jobs SET status=%s,qa_result=%s::jsonb,
                updated_at=now() WHERE job_id=%s AND status='qa_pending'
                AND artifact_uri IS NOT NULL RETURNING job_id''',
                (status,json.dumps(report_json),job_id)).fetchone()
        return bool(row)

    def approve(self, job_id, *, human, rights, employee_authorized):
        if not (human is True and rights is True and employee_authorized is True):
            return False
        with self.conn.transaction():
            row=self.conn.execute('''UPDATE automation_jobs SET status='ready',
                handoff_status='ready',updated_at=now() WHERE job_id=%s
                AND status='human_review' AND qa_result IS NOT NULL
                RETURNING job_id''',(job_id,)).fetchone()
        return bool(row)
