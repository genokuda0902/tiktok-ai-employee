"""Independent status/authorization boundary for manual TikTok posting.

Only a trusted server-side authentication adapter may construct Principal. Never
construct it from browser-submitted employee IDs. No TikTok API or file sharing.
"""
from dataclasses import dataclass
from typing import Protocol

GENERATING = '動画生成待ち'
QA_WAIT = '品質検査待ち'
QA_FAILED = '品質検査不合格'
ADMIN_WAIT = '管理者承認待ち'
ASSIGNED = '投稿担当者割当済み'
EMPLOYEE_WAIT = '社員確認待ち'
REVISION = '修正依頼'
APPROVED = '投稿承認済み'
MANUAL_WAIT = '手動投稿待ち'
URL_WAIT = '投稿URL確認待ち'
DONE = '社員による手動投稿完了'
CANCELLED = '投稿中止'

class Forbidden(PermissionError):
    pass

class InvalidTransition(ValueError):
    pass

@dataclass(frozen=True)
class Principal:
    user_id: str
    role: str
    authenticated: bool
    approved: bool
    active: bool

    def require(self, admin=False):
        if not self.authenticated or not self.approved or not self.active or not self.user_id:
            raise Forbidden('Authenticated, approved, active employee required')
        if admin and self.role != 'admin':
            raise Forbidden('Administrator required')

@dataclass(frozen=True)
class PostingRecord:
    video_id: str
    account_id: str
    status: str
    qa_passed: bool
    assets_approved: bool
    approved_by: str = ''
    assignee: str = ''
    post_reference: str = ''

class PrivateDrive(Protocol):
    """Implemented by engine ②. No anyone/public permission is permitted."""
    def grant_private(self, file_id: str, employee_id: str) -> None: ...
    def revoke_private(self, file_id: str, employee_id: str) -> None: ...
    def get_private(self, file_id: str, employee_id: str) -> bytes: ...

TRANSITIONS = {
    GENERATING: {QA_WAIT},
    QA_WAIT: {QA_FAILED, ADMIN_WAIT},
    QA_FAILED: {QA_WAIT, CANCELLED},
    ADMIN_WAIT: {ASSIGNED, REVISION, CANCELLED},
    ASSIGNED: {EMPLOYEE_WAIT, REVISION, CANCELLED},
    EMPLOYEE_WAIT: {APPROVED, REVISION, CANCELLED},
    REVISION: {QA_WAIT, CANCELLED},
    APPROVED: {MANUAL_WAIT, REVISION, CANCELLED},
    MANUAL_WAIT: {URL_WAIT, REVISION, CANCELLED},
    URL_WAIT: {DONE, REVISION, CANCELLED},
    DONE: set(),
    CANCELLED: set(),
}
ADMIN_ONLY = {QA_FAILED, ADMIN_WAIT, ASSIGNED, CANCELLED, DONE}

def transition(record: PostingRecord, actor: Principal, target: str, *, post_reference: str = '') -> PostingRecord:
    """Pure transition: caller persists state + actor audit in ONE database transaction."""
    actor.require(admin=target in ADMIN_ONLY)
    if target not in TRANSITIONS.get(record.status, set()):
        raise InvalidTransition(f'{record.status} -> {target} forbidden')
    if actor.role != 'admin' and actor.user_id != record.assignee:
        raise Forbidden('Not assigned to this employee')
    if target in {ASSIGNED, EMPLOYEE_WAIT, APPROVED, MANUAL_WAIT, URL_WAIT, DONE}:
        if not record.qa_passed or not record.assets_approved or not record.approved_by:
            raise InvalidTransition('QA, assets and administrator approval required')
        if not record.assignee:
            raise InvalidTransition('Assigned employee required')
    if target == ADMIN_WAIT and (not record.qa_passed or not record.assets_approved):
        raise InvalidTransition('Failed QA or unapproved assets')
    if target == DONE and not (record.post_reference or post_reference):
        raise InvalidTransition('Manual post URL or post ID required')
    from dataclasses import replace
    return replace(record, status=target, post_reference=post_reference or record.post_reference)

def authorize_download(record: PostingRecord, actor: Principal, file_id: str, drive: PrivateDrive) -> bytes:
    actor.require()
    if actor.user_id != record.assignee or record.status not in {EMPLOYEE_WAIT, APPROVED, MANUAL_WAIT}:
        raise Forbidden('Not your approved video')
    if not record.qa_passed or not record.assets_approved or not record.approved_by or not file_id:
        raise Forbidden('Unsafe or missing private media')
    return drive.get_private(file_id, actor.user_id)
