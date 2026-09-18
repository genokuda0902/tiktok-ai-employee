"""Employee registry: trusted server-side storage only; expose via AuthenticatedService."""
import re
import sqlite3
import uuid
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat()


class Denied(PermissionError):
    pass


class Registry:
    def __init__(self, database=':memory:'):
        self.db = sqlite3.connect(database)
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS employees (
          id TEXT PRIMARY KEY, email TEXT NOT NULL UNIQUE COLLATE NOCASE,
          status TEXT NOT NULL CHECK(status IN ('pending','approved','rejected','suspended')),
          role TEXT NOT NULL CHECK(role IN ('employee','admin')),
          created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS identities (
          provider TEXT NOT NULL, subject TEXT NOT NULL, employee_id TEXT NOT NULL UNIQUE REFERENCES employees(id),
          PRIMARY KEY(provider,subject));
        CREATE TABLE IF NOT EXISTS accounts (
          id TEXT PRIMARY KEY, employee_id TEXT NOT NULL REFERENCES employees(id),
          handle TEXT NOT NULL UNIQUE COLLATE NOCASE);
        CREATE TABLE IF NOT EXISTS jobs (
          id TEXT PRIMARY KEY, employee_id TEXT NOT NULL REFERENCES employees(id),
          account_id TEXT NOT NULL REFERENCES accounts(id),
          status TEXT NOT NULL CHECK(status IN ('requested','generating','qa_failed','ready','revision','posted')),
          artifact_ref TEXT, post_url TEXT, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS audit (
          id TEXT PRIMARY KEY, actor_id TEXT NOT NULL, actor_subject TEXT NOT NULL,
          action TEXT NOT NULL, target_id TEXT NOT NULL, created_at TEXT NOT NULL);
        ''')

    def _actor(self, actor_id):
        row = self.db.execute('SELECT role,status FROM employees WHERE id=?', (actor_id,)).fetchone()
        if not row or row[1] != 'approved':
            raise Denied('actor is not approved')
        return row[0]

    def _admin(self, actor_id):
        if self._actor(actor_id) != 'admin':
            raise Denied('admin required')

    def _audit(self, actor, action, target):
        subject = self.db.execute('SELECT subject FROM identities WHERE employee_id=?', (actor,)).fetchone()
        self.db.execute('INSERT INTO audit VALUES(?,?,?,?,?,?)', (uuid.uuid4().hex, actor, subject[0] if subject else 'UNBOUND_LOCAL_ONLY', action, target, now()))

    def bootstrap_admin(self, employee_id, email, google_subject=None):
        """Offline one-time trusted setup; never expose as an HTTP/form endpoint."""
        if self.db.execute('SELECT COUNT(*) FROM employees').fetchone()[0]:
            raise Denied('bootstrap disabled after first employee')
        self._insert(employee_id, email, 'approved', 'admin')
        if google_subject:
            self.bind_identity(employee_id, google_subject)
        self.db.commit()

    def _insert(self, employee_id, email, status, role):
        email = email.strip().lower()
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
            raise ValueError('invalid email')
        if not re.fullmatch(r'[a-zA-Z0-9_-]{1,64}', employee_id):
            raise ValueError('invalid employee id')
        self.db.execute('INSERT INTO employees VALUES(?,?,?,?,?)', (employee_id, email, status, role, now()))

    def bind_identity(self, employee_id, google_subject):
        """Trusted server operation only, after Google ID token verification and admin approval."""
        if not isinstance(google_subject, str) or not re.fullmatch(r'[0-9]{1,255}', google_subject):
            raise ValueError('invalid Google subject')
        self.db.execute('INSERT INTO identities VALUES(?,?,?)', ('google', google_subject, employee_id))

    def resolve_identity(self, google_subject):
        row = self.db.execute('SELECT employee_id FROM identities WHERE provider=? AND subject=?', ('google', google_subject)).fetchone()
        if not row:
            raise Denied('identity not linked')
        self._actor(row[0])
        return row[0]

    def register(self, employee_id, email):
        with self.db:
            self._insert(employee_id, email, 'pending', 'employee')
        return employee_id

    def decide(self, admin_id, employee_id, decision):
        self._admin(admin_id)
        if decision not in ('approved', 'rejected', 'suspended'):
            raise ValueError('invalid decision')
        with self.db:
            cur = self.db.execute("UPDATE employees SET status=? WHERE id=? AND role='employee'", (decision, employee_id))
            if cur.rowcount != 1:
                raise ValueError('employee not found or protected')
            self._audit(admin_id, 'employee.' + decision, employee_id)

    def change_role(self, admin_id, employee_id, role):
        self._admin(admin_id)
        if role not in ('employee', 'admin') or admin_id == employee_id:
            raise Denied('invalid role change')
        with self.db:
            cur = self.db.execute('UPDATE employees SET role=? WHERE id=?', (role, employee_id))
            if cur.rowcount != 1:
                raise ValueError('employee not found')
            self._audit(admin_id, 'employee.role.' + role, employee_id)

    def link_account(self, actor_id, employee_id, account_id, handle):
        self._admin(actor_id)
        self._actor(employee_id)
        if not re.fullmatch(r'[A-Za-z0-9_.]{1,64}', handle):
            raise ValueError('invalid handle')
        with self.db:
            self.db.execute('INSERT INTO accounts VALUES(?,?,?)', (account_id, employee_id, handle))
            self._audit(actor_id, 'account.linked', account_id)

    def request(self, actor_id, account_id):
        self._actor(actor_id)
        owner = self.db.execute('SELECT employee_id FROM accounts WHERE id=?', (account_id,)).fetchone()
        if not owner or owner[0] != actor_id:
            raise Denied('account is not yours')
        job_id = uuid.uuid4().hex
        with self.db:
            self.db.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?,?,?)', (job_id, actor_id, account_id, 'requested', None, None, now()))
            self._audit(actor_id, 'job.requested', job_id)
        return job_id

    def set_generation_result(self, admin_id, job_id, status, artifact_ref=None):
        self._admin(admin_id)
        if status not in ('generating', 'qa_failed', 'ready'):
            raise ValueError('invalid engine status')
        if status == 'ready' and not artifact_ref:
            raise ValueError('ready requires artifact reference')
        with self.db:
            cur = self.db.execute("UPDATE jobs SET status=?,artifact_ref=? WHERE id=? AND status IN ('requested','generating','revision')", (status, artifact_ref, job_id))
            if cur.rowcount != 1:
                raise ValueError('invalid job transition')
            self._audit(admin_id, 'job.' + status, job_id)

    def review(self, actor_id, job_id, decision, post_url=None):
        self._actor(actor_id)
        if decision not in ('revision', 'posted'):
            raise ValueError('invalid review decision')
        if decision == 'posted' and (not post_url or not re.fullmatch(r'https://(?:www\.)?tiktok\.com/@[A-Za-z0-9_.]+/video/[0-9]+', post_url)):
            raise ValueError('manual TikTok post URL required')
        if decision == 'revision' and post_url:
            raise ValueError('revision cannot have post URL')
        with self.db:
            cur = self.db.execute("UPDATE jobs SET status=?,post_url=? WHERE id=? AND employee_id=? AND status='ready'", (decision, post_url, job_id, actor_id))
            if cur.rowcount != 1:
                raise Denied('job is not yours or not ready')
            self._audit(actor_id, 'job.' + decision, job_id)

    def history(self, actor_id, employee_id=None):
        role = self._actor(actor_id)
        target = employee_id or actor_id
        if role != 'admin' and target != actor_id:
            raise Denied('cross-employee access')
        return self.db.execute('SELECT id,account_id,status,artifact_ref,post_url,created_at FROM jobs WHERE employee_id=? ORDER BY created_at,id', (target,)).fetchall()

    def job_for_employee(self, actor_id, job_id):
        role = self._actor(actor_id)
        row = self.db.execute('SELECT id,employee_id,account_id,status,artifact_ref,post_url FROM jobs WHERE id=?', (job_id,)).fetchone()
        if not row or (role != 'admin' and row[1] != actor_id):
            raise Denied('job not accessible')
        return row
