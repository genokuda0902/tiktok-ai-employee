import sqlite3
import unittest
from employee_management.core import Registry, Denied
from employee_management.auth import AuthenticatedService, GoogleVerifier


class FakeVerifiedGoogle:
    """TEST ONLY: simulates an already cryptographically verified Google token."""
    def verify(self, token):
        subjects = {'admin-token': '100000000000000000001'}
        subjects.update({f'person-{n}-token': str(100000000000000000001+n) for n in range(1, 7)})
        if token not in subjects:
            raise Denied('authentication required')
        return subjects[token]


class EmployeeManagementTests(unittest.TestCase):
    def setUp(self):
        self.r = Registry()
        self.r.bootstrap_admin('admin', 'admin@example.test', '100000000000000000001')
        self.s = AuthenticatedService(self.r, FakeVerifiedGoogle())
        for n in range(1, 7):
            self.r.register(f'person{n}', f'person{n}@example.test')
            self.s.assign_identity('admin-token', f'person{n}', f'person-{n}-token')

    def approve(self, n):
        self.s.decide('admin-token', f'person{n}', 'approved')
        self.s.link_account('admin-token', f'person{n}', f'account{n}', f'handle{n}')

    def test_unauthenticated_denied_on_history_video_and_admin(self):
        self.approve(1)
        job = self.s.request('person-1-token', 'account1')
        for operation in (lambda: self.s.history(None), lambda: self.s.video('', job),
                          lambda: self.s.decide('forged', 'person2', 'approved')):
            with self.assertRaises(Denied): operation()

    def test_pending_denied_on_request_video_history(self):
        self.approve(1)
        job = self.s.request('person-1-token', 'account1')
        for operation in (lambda: self.s.request('person-2-token', 'account1'),
                          lambda: self.s.video('person-2-token', job),
                          lambda: self.s.history('person-2-token')):
            with self.assertRaises(Denied): operation()

    def test_six_employee_cross_access_and_modification_denied(self):
        for n in range(1, 7): self.approve(n)
        jobs = [self.s.request(f'person-{n}-token', f'account{n}') for n in range(1, 7)]
        for n in range(1, 7):
            other = n % 6 + 1
            with self.assertRaises(Denied): self.s.video(f'person-{n}-token', jobs[other-1])
            with self.assertRaises(Denied): self.s.history(f'person-{n}-token', f'person{other}')
            with self.assertRaises(Denied): self.s.request(f'person-{n}-token', f'account{other}')
            self.r.set_generation_result('admin', jobs[other-1], 'ready', 'internal-artifact-ref')
            with self.assertRaises(Denied): self.s.review(f'person-{n}-token', jobs[other-1], 'posted', f'https://www.tiktok.com/@handle{other}/video/123')

    def test_employee_cannot_approve_or_change_role(self):
        self.approve(1)
        with self.assertRaises(Denied): self.s.decide('person-1-token', 'person2', 'approved')
        with self.assertRaises(Denied): self.s.change_role('person-1-token', 'person2', 'admin')

    def test_admin_approve_suspend_and_change_role(self):
        self.s.decide('admin-token', 'person1', 'approved')
        self.s.change_role('admin-token', 'person1', 'admin')
        self.assertEqual(self.r.db.execute("SELECT role FROM employees WHERE id='person1'").fetchone()[0], 'admin')
        self.s.change_role('admin-token', 'person1', 'employee')
        self.s.decide('admin-token', 'person1', 'suspended')
        with self.assertRaises(Denied): self.s.history('person-1-token')

    def test_duplicate_registration_and_identity_binding(self):
        with self.assertRaises(sqlite3.IntegrityError): self.r.register('other', 'PERSON1@example.test')
        with self.assertRaises(sqlite3.IntegrityError): self.r.register('person1', 'other@example.test')
        with self.assertRaises(sqlite3.IntegrityError): self.s.assign_identity('admin-token', 'person2', 'person-1-token')

    def test_suspended_cannot_relogin_with_same_verified_subject(self):
        self.approve(1)
        self.s.decide('admin-token', 'person1', 'suspended')
        for operation in (lambda: self.s.history('person-1-token'), lambda: self.s.request('person-1-token', 'account1')):
            with self.assertRaises(Denied): operation()

    def test_audit_uses_verified_subject_not_claimed_employee_id(self):
        self.approve(1)
        self.s.request('person-1-token', 'account1')
        row = self.r.db.execute("SELECT actor_id,actor_subject FROM audit WHERE action='job.requested'").fetchone()
        self.assertEqual(row, ('person1', '100000000000000000002'))

    def test_manual_post_only_and_context(self):
        self.approve(1)
        job = self.s.request('person-1-token', 'account1')
        with self.assertRaises(Denied): self.s.review('person-1-token', job, 'posted', 'https://www.tiktok.com/@handle1/video/123')
        self.r.set_generation_result('admin', job, 'ready', 'internal-artifact-ref')
        context = self.s.posting_context('person-1-token', job)
        self.assertEqual(context['employee_id'], 'person1')
        self.assertTrue(context['manual_post_only'])
        self.s.review('person-1-token', job, 'posted', 'https://www.tiktok.com/@handle1/video/123')
        self.assertEqual(self.s.history('person-1-token')[0][2], 'posted')

    def test_google_verifier_requires_client_id_and_rejects_missing_token(self):
        with self.assertRaises(ValueError): GoogleVerifier('')
        with self.assertRaises(Denied): GoogleVerifier('test-client').verify('')

    def test_no_second_admin_bootstrap(self):
        with self.assertRaises(Denied): self.r.bootstrap_admin('other', 'other@example.test')


if __name__ == '__main__': unittest.main()
