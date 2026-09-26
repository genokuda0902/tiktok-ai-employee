"""Durable review-only orchestrator. Caller supplies a cryptographically verified identity adapter.

This module has no TikTok publishing or public file-sharing capability.
"""
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from employee_management.auth import AuthenticatedService
from employee_management.core import Denied
from src.manual_posting_flow import PostingRecord, Principal, transition, QA_WAIT, QA_FAILED, REVISION
from video_engine.production_v2.pipeline import request_revision

STATES = ('GENERATED','QUALITY_CHECK','HUMAN_REVIEW','REVISION_REQUESTED','REGENERATING','APPROVED_FOR_MANUAL_POST','MANUALLY_POSTED')
METRICS = ('views','three_second_views','average_watch_time','completion_rate','likes','saves','shares','comments','followers_gained')

def compare_variants(rows):
    """Compare matched variants without treating missing data as zero or views as a winner."""
    by_variant={v:[] for v in ('A','B','C')}
    for item in rows:
        if item['variant'] in by_variant:by_variant[item['variant']].append(item['metrics'])
    summary={}
    for variant,items in by_variant.items():
        measured=[m for m in items if m['views'] is not None and m['three_second_views'] is not None and m['completion_rate'] is not None]
        summary[variant]={'samples':len(items),'measured':len(measured),'three_second_rate':None,'completion_rate':None,'engagement_rate':None}
        if measured:
            views=sum(m['views'] for m in measured)
            if views:
                summary[variant]['three_second_rate']=sum(m['three_second_views'] for m in measured)/views
                if all(m[k] is not None for m in measured for k in ('likes','saves','shares','comments')):
                    summary[variant]['engagement_rate']=sum(sum(m[k] for k in ('likes','saves','shares','comments')) for m in measured)/views
            summary[variant]['completion_rate']=sum(m['completion_rate'] for m in measured)/len(measured)
    # Age-matched real posts and >=10 samples per variant must be verified separately.
    return {'variants':summary,'winner':None,'status':'INSUFFICIENT_COMPARABLE_EVIDENCE'}

def now(): return datetime.now(timezone.utc).isoformat()

class Store:
    def __init__(self, path, identity:AuthenticatedService):
        self.identity=identity
        self.db=sqlite3.connect(path)
        self.db.row_factory=sqlite3.Row
        self.db.executescript('''
          PRAGMA foreign_keys=ON;
          CREATE TABLE IF NOT EXISTS videos(video_id TEXT PRIMARY KEY,trace_id TEXT UNIQUE NOT NULL,employee_id TEXT NOT NULL,account_id TEXT NOT NULL,version INTEGER NOT NULL,sha256 TEXT NOT NULL,drive_file_id TEXT NOT NULL,quality_status TEXT NOT NULL,posting_state TEXT NOT NULL,created_at TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS revisions(revision_id TEXT PRIMARY KEY,video_id TEXT NOT NULL REFERENCES videos(video_id),trace_id TEXT NOT NULL,actor TEXT NOT NULL,scene_id INTEGER NOT NULL,old_version INTEGER NOT NULL,new_version INTEGER NOT NULL,instruction TEXT NOT NULL,status TEXT NOT NULL,at TEXT NOT NULL,UNIQUE(video_id,new_version));
          CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,video_id TEXT NOT NULL,trace_id TEXT NOT NULL,actor TEXT NOT NULL,action TEXT NOT NULL,at TEXT NOT NULL,details TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS analytics(video_id TEXT NOT NULL,trace_id TEXT NOT NULL,variant TEXT NOT NULL,source TEXT NOT NULL,metrics_json TEXT NOT NULL,at TEXT NOT NULL,PRIMARY KEY(video_id,variant,source));
          CREATE TABLE IF NOT EXISTS idempotency(key TEXT PRIMARY KEY,video_id TEXT NOT NULL);
        ''')
    def actor(self,token): return self.identity._actor(token) # verifies signed ID token via configured verifier
    def _video(self,video_id):
        row=self.db.execute('SELECT * FROM videos WHERE video_id=?',(video_id,)).fetchone()
        if row is None: raise ValueError('Video not found')
        return row
    def _audit(self,row,actor,action,details=''):
        self.db.execute('INSERT INTO audit(video_id,trace_id,actor,action,at,details) VALUES(?,?,?,?,?,?)',(row['video_id'],row['trace_id'],actor,action,now(),details))
    def register(self,token,video_id,trace_id,employee_id,account_id,version,digest,drive_id,quality,idempotency_key):
        admin=self.actor(token);self.identity.registry._admin(admin)
        if not digest or len(digest)!=64 or not drive_id or quality!='QUALITY_NOT_APPROVED': raise ValueError('Unapproved test receipt required')
        self.identity.registry._actor(employee_id)
        with self.db:
            if self.db.execute('SELECT 1 FROM idempotency WHERE key=?',(idempotency_key,)).fetchone(): raise ValueError('Duplicate operation')
            self.db.execute('INSERT INTO videos VALUES(?,?,?,?,?,?,?,?,?,?)',(video_id,trace_id,employee_id,account_id,version,digest,drive_id,quality,'HUMAN_REVIEW',now()))
            self.db.execute('INSERT INTO idempotency VALUES(?,?)',(idempotency_key,video_id))
            self._audit(self._video(video_id),admin,'drive_received',drive_id)
    def revision(self,token,plan,req):
        actor=self.actor(token); row=self._video(req['video_id'])
        if row['employee_id']!=actor and self.identity.registry._actor(actor)!='admin': raise Denied('Not assigned')
        if row['version']!=req['previous_version'] or row['trace_id']!=req['trace_id'] or row['quality_status']!='QUALITY_NOT_APPROVED': raise ValueError('Stale or invalid revision')
        if req['revision_id'] in (None,''): raise ValueError('revision_id required')
        if req['requested_by']!=actor: raise Denied('Impersonation')
        revised=request_revision(plan,req,actor)
        with self.db:
            self.db.execute('INSERT INTO revisions VALUES(?,?,?,?,?,?,?,?,?,?)',(req['revision_id'],row['video_id'],row['trace_id'],actor,req['scene_id'],row['version'],revised['version'],req['instruction'],'REGENERATING',now()))
            self.db.execute('UPDATE videos SET posting_state=? WHERE video_id=?',('REGENERATING',row['video_id']))
            self._audit(row,actor,'revision.requested',req['revision_id'])
        return revised
    def regenerated(self,token,video_id,revision_id,new_digest,new_drive_id,qa):
        admin=self.actor(token); self.identity.registry._admin(admin);row=self._video(video_id)
        rev=self.db.execute('SELECT * FROM revisions WHERE revision_id=? AND video_id=?',(revision_id,video_id)).fetchone()
        if not rev or rev['status']!='REGENERATING' or row['posting_state']!='REGENERATING': raise ValueError('No pending revision')
        if not new_drive_id or qa.get('sha256')!=new_digest or qa.get('quality_status')!='QUALITY_NOT_APPROVED': raise ValueError('New immutable media evidence required')
        with self.db:
            self.db.execute('UPDATE videos SET version=?,sha256=?,drive_file_id=?,quality_status=?,posting_state=? WHERE video_id=?',(rev['new_version'],new_digest,new_drive_id,'QUALITY_NOT_APPROVED','HUMAN_REVIEW',video_id))
            self.db.execute('UPDATE revisions SET status=? WHERE revision_id=?',('RE_QA_REVIEW',revision_id))
            self._audit(row,admin,'revision.regenerated',revision_id)
    def attempt_post_approval(self,token,video_id):
        actor=self.actor(token);self.identity.registry._admin(actor);row=self._video(video_id)
        if row['quality_status']!='PUBLICATION_APPROVED':
            with self.db:self._audit(row,actor,'approval.denied','QUALITY_NOT_APPROVED')
            raise Denied('Publication approval and human rights review required')
        raise Denied('Production approval integration unavailable; fail closed')
    def record_metrics(self,token,video_id,variant,source,metrics):
        actor=self.actor(token);self.identity.registry._admin(actor);row=self._video(video_id)
        if source!='TEST_FIXTURE' and row['posting_state']!='MANUALLY_POSTED': raise ValueError('Unposted video has no real analytics')
        if not all(k in metrics for k in METRICS): raise ValueError('Incomplete nullable metrics')
        for k in METRICS:
            v=metrics[k]
            if v is not None and (not isinstance(v,(int,float)) or v<0): raise ValueError('Invalid metric')
        with self.db:
            self.db.execute('INSERT INTO analytics VALUES(?,?,?,?,?,?)',(video_id,row['trace_id'],variant,source,json.dumps(metrics),now()))
            self._audit(row,actor,'analytics.fixture' if source=='TEST_FIXTURE' else 'analytics.recorded',variant)
    def feedback(self,token,video_id):
        actor=self.actor(token);row=self._video(video_id)
        if actor!=row['employee_id'] and self.identity.registry._actor(actor)!='admin': raise Denied('Not assigned')
        items=self.db.execute('SELECT variant,source,metrics_json FROM analytics WHERE video_id=?',(video_id,)).fetchall()
        source='TEST_FIXTURE' if items and all(x['source']=='TEST_FIXTURE' for x in items) else 'NONE'
        source_metrics=[{**dict(x),'metrics':json.loads(x['metrics_json'])} for x in items]
        return {'video_id':video_id,'trace_id':row['trace_id'],'data_type':source,'recommended_hook':None,'recommended_duration':None,'recommended_structure':None,'recommended_cta':None,'recommended_asset_type':None,'recommended_audio_style':None,'recommended_visual_style':None,'recommended_posting_time':None,'reason':'Insufficient real comparable metrics; test candidate hooks without declaring a winner.','source_metrics':source_metrics,'comparison':compare_variants(source_metrics)}

def load_feedback(plan,feedback):
    if plan['video_id']!=feedback['video_id'] or plan['trace_id']!=feedback['trace_id']: raise ValueError('Wrong trace')
    return {**plan,'prior_feedback':feedback}
