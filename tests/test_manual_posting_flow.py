import unittest
from dataclasses import replace
from src.manual_posting_flow import (
    Principal, PostingRecord, Forbidden, InvalidTransition, transition,
    authorize_download, QA_WAIT, QA_FAILED, ADMIN_WAIT, ASSIGNED,
    EMPLOYEE_WAIT, APPROVED, MANUAL_WAIT, URL_WAIT, DONE, REVISION, CANCELLED,
)

ADMIN = Principal('admin', 'admin', True, True, True)
ALICE = Principal('alice', 'employee', True, True, True)
BOB = Principal('bob', 'employee', True, True, True)
INACTIVE = Principal('alice', 'employee', True, True, False)
ANON = Principal('alice', 'employee', False, True, True)

class DriveMock:
    def __init__(self):
        self.permissions = {'alice'}
    def get_private(self, file_id, employee_id):
        if employee_id not in self.permissions or file_id != 'private-file':
            raise Forbidden('Drive permission denied')
        return b'mock private video'

class FlowTests(unittest.TestCase):
    def setUp(self):
        self.record = PostingRecord('video1', 'account1', QA_WAIT, True, True, 'admin', 'alice')

    def test_qa_failed_cannot_approve(self):
        failed = replace(self.record, status=QA_FAILED, qa_passed=False)
        with self.assertRaises(InvalidTransition):
            transition(failed, ADMIN, APPROVED)
        with self.assertRaises(InvalidTransition):
            transition(failed, ADMIN, ADMIN_WAIT)

    def test_happy_path_and_manual_post_proof(self):
        r = transition(self.record, ADMIN, ADMIN_WAIT)
        r = transition(r, ADMIN, ASSIGNED)
        r = transition(r, ALICE, EMPLOYEE_WAIT)
        r = transition(r, ALICE, APPROVED)
        r = transition(r, ALICE, MANUAL_WAIT)
        r = transition(r, ALICE, URL_WAIT)
        with self.assertRaises(InvalidTransition):
            transition(r, ADMIN, DONE)
        r = transition(r, ADMIN, DONE, post_reference='https://www.tiktok.com/@alice/video/123')
        self.assertEqual(r.status, DONE)
        with self.assertRaises(InvalidTransition):
            transition(r, ADMIN, DONE)

    def test_revision_and_cancel(self):
        r = transition(self.record, ADMIN, ADMIN_WAIT)
        r = transition(r, ADMIN, REVISION)
        self.assertEqual(transition(r, ADMIN, QA_WAIT).status, QA_WAIT)
        self.assertEqual(transition(r, ADMIN, CANCELLED).status, CANCELLED)

    def test_cross_employee_denied(self):
        r = replace(self.record, status=ASSIGNED)
        with self.assertRaises(Forbidden):
            transition(r, BOB, EMPLOYEE_WAIT)
        with self.assertRaises(Forbidden):
            authorize_download(r, BOB, 'private-file', DriveMock())

    def test_non_admin_approval_denied(self):
        r = replace(self.record, status=QA_WAIT)
        with self.assertRaises(Forbidden):
            transition(r, ALICE, ADMIN_WAIT)

    def test_unauthenticated_and_inactive_denied(self):
        r = replace(self.record, status=EMPLOYEE_WAIT)
        for principal in (ANON, INACTIVE):
            with self.assertRaises(Forbidden):
                authorize_download(r, principal, 'private-file', DriveMock())

    def test_drive_mock_private_access(self):
        r = replace(self.record, status=EMPLOYEE_WAIT)
        self.assertEqual(authorize_download(r, ALICE, 'private-file', DriveMock()), b'mock private video')
        with self.assertRaises(Forbidden):
            authorize_download(r, ALICE, 'wrong-file', DriveMock())
        with self.assertRaises(Forbidden):
            authorize_download(replace(r, qa_passed=False), ALICE, 'private-file', DriveMock())

if __name__ == '__main__':
    unittest.main()
