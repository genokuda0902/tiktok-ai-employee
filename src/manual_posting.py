"""Manual-only posting registry. No TikTok API, uploads, or public file serving.

The caller MUST authenticate the actor server-side and supply an approved roster
from the employee-management service. Never accept actor/role from browser input.
This library is NOT a deployed authentication service or employee download portal.
"""
import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

GENERATING = '動画生成待ち'
QA_WAIT = '品質検査待ち'
ADMIN_WAIT = '管理者承認待ち'
ASSIGNED = '投稿担当者割当済み'
READY = '手動投稿待ち'
DONE = '投稿完了'
RETURNED = '差し戻し'
FAILED = '投稿失敗'
URL_WAIT = '投稿URL確認待ち'

class Rejected(ValueError):
    pass

def now():
    return datetime.now(timezone.utc).isoformat()

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

class Registry:
    def __init__(self, db_path, roster):
        """roster: trusted server-side {employee_id: {'approved': bool, 'role': 'admin'|'employee'}}."""
        self.roster = roster
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY, account_id TEXT NOT NULL, digest TEXT NOT NULL,
            path TEXT NOT NULL, status TEXT NOT NULL, qa_pass INTEGER NOT NULL,
            asset_approved INTEGER NOT NULL, approved_by TEXT, assignee TEXT,
            post_url TEXT, posted_at TEXT, url_verified INTEGER NOT NULL DEFAULT 0,
            UNIQUE(account_id,digest));
          CREATE TABLE IF NOT EXISTS audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT, video_id TEXT NOT NULL,
            actor TEXT NOT NULL, action TEXT NOT NULL, at TEXT NOT NULL,
            details TEXT NOT NULL);
          CREATE UNIQUE INDEX IF NOT EXISTS unique_post_url ON videos(post_url)
            WHERE post_url IS NOT NULL;
        ''')
        self.db.commit()

    def _actor(self, actor, admin=False):
        user = self.roster.get(actor)
        if not user or user.get('approved') is not True:
            raise Rejected('Unapproved employee')
        if admin and user.get('role') != 'admin':
            raise Rejected('Administrator required')

    def _get(self, video_id):
        row = self.db.execute('SELECT * FROM videos WHERE id=?', (video_id,)).fetchone()
        if row is None:
            raise Rejected('Video not found')
        return row

    def _log(self, video_id, actor, action, details=''):
        self.db.execute('INSERT INTO audit(video_id,actor,action,at,details) VALUES(?,?,?,?,?)',
                        (video_id, actor, action, now(), details))

    def register(self, actor, video_id, account_id, path, qa_report, asset_approved):
        self._actor(actor, admin=True)
        file = Path(path).resolve(strict=True)
        if file.suffix.lower() != '.mp4' or not file.is_file() or file.stat().st_size == 0:
            raise Rejected('Valid MP4 required')
        digest = sha256(file)
        # A trusted QA report must bind its result to the exact media bytes.
        passed = qa_report.get('passed') is True and qa_report.get('sha256') == digest
        if not passed or asset_approved is not True:
            raise Rejected('QA, hash or asset approval failed')
        try:
            with self.db:
                self.db.execute('INSERT INTO videos(id,account_id,digest,path,status,qa_pass,asset_approved) VALUES(?,?,?,?,?,?,?)',
                                (video_id, account_id, digest, str(file), ADMIN_WAIT, 1, 1))
                self._log(video_id, actor, 'register')
        except sqlite3.IntegrityError as exc:
            raise Rejected('Duplicate video ID or account/media combination') from exc

    def approve(self, actor, video_id):
        self._actor(actor, admin=True)
        row = self._get(video_id)
        if row['status'] != ADMIN_WAIT or not row['qa_pass'] or not row['asset_approved']:
            raise Rejected('Not eligible for approval')
        with self.db:
            self.db.execute('UPDATE videos SET approved_by=? WHERE id=?', (actor, video_id))
            self._log(video_id, actor, 'approve')

    def assign(self, actor, video_id, employee):
        self._actor(actor, admin=True)
        self._actor(employee)
        row = self._get(video_id)
        if row['status'] != ADMIN_WAIT or not row['approved_by']:
            raise Rejected('Administrator approval required')
        with self.db:
            self.db.execute('UPDATE videos SET assignee=?,status=? WHERE id=?', (employee, ASSIGNED, video_id))
            self._log(video_id, actor, 'assign', employee)

    def review(self, actor, video_id):
        self._actor(actor)
        row = self._get(video_id)
        if row['assignee'] != actor or row['status'] != ASSIGNED:
            raise Rejected('Not your assigned video')
        if sha256(row['path']) != row['digest']:
            raise Rejected('Media changed after QA')
        with self.db:
            self.db.execute('UPDATE videos SET status=? WHERE id=?', (READY, video_id))
            self._log(video_id, actor, 'review')
        # Caller must separately enforce private, authenticated download authorization.
        return row['path']

    def report(self, actor, video_id, url, posted_at):
        self._actor(actor)
        row = self._get(video_id)
        if row['assignee'] != actor or row['status'] != READY:
            raise Rejected('Not your ready video or already reported')
        if not url or not isinstance(url, str):
            raise Rejected('Post URL required; keep manual posting pending')
        parsed = urlparse(url)
        if parsed.scheme != 'https' or parsed.hostname not in ('www.tiktok.com', 'tiktok.com') or not re.fullmatch(r'/@[^/]+/video/\d+', parsed.path):
            raise Rejected('Canonical TikTok video URL required')
        try:
            datetime.fromisoformat(posted_at.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            raise Rejected('Valid posting timestamp required')
        try:
            with self.db:
                self.db.execute('UPDATE videos SET status=?,post_url=?,posted_at=?,url_verified=0 WHERE id=?',
                                (URL_WAIT, url, posted_at, video_id))
                self._log(video_id, actor, 'report', 'URL requires administrator verification')
        except sqlite3.IntegrityError as exc:
            raise Rejected('Duplicate post URL') from exc

    def verify(self, actor, video_id, account_matches):
        self._actor(actor, admin=True)
        row = self._get(video_id)
        if row['status'] != URL_WAIT or account_matches is not True:
            raise Rejected('Manual account ownership verification required')
        with self.db:
            self.db.execute('UPDATE videos SET status=?,url_verified=1 WHERE id=?', (DONE, video_id))
            self._log(video_id, actor, 'verify_post')

    def history(self, actor, video_id=None):
        self._actor(actor)
        if self.roster[actor].get('role') == 'admin':
            if video_id:
                return [dict(x) for x in self.db.execute('SELECT * FROM videos WHERE id=?', (video_id,))]
            return [dict(x) for x in self.db.execute('SELECT * FROM videos ORDER BY rowid DESC')]
        return [dict(x) for x in self.db.execute('SELECT id,account_id,status,post_url,posted_at FROM videos WHERE assignee=? AND (? IS NULL OR id=?)', (actor, video_id, video_id))]

    def audit(self, actor, video_id=None):
        self._actor(actor, admin=True)
        return [dict(x) for x in self.db.execute('SELECT * FROM audit WHERE (? IS NULL OR video_id=?) ORDER BY id', (video_id, video_id))]
