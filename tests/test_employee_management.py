import sqlite3
import unittest
from employee_management.core import Registry, Denied


class EmployeeManagementTests(unittest.TestCase):
    def setUp(self):
        self.r = Registry()
        self.r.bootstrap_admin('admin', 'admin@example.test')
        self.r.register('alice', 'alice@example.test')
        self.r.register('bob', 'bob@example.test')

    def test_pending_cannot_request(self):
        with self.assertRaises(Denied):
            self.r.request('alice', 'account-a')

    def test_duplicate_email_and_id(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.r.register('other', 'ALICE@example.test')
        with self.assertRaises(sqlite3.IntegrityError):
            self.r.register('alice', 'different@example.test')

    def test_employee_cannot_approve(self):
        self.r.decide('admin', 'alice', 'approved')
        with self.assertRaises(Denied):
            self.r.decide('alice', 'bob', 'approved')

    def test_cross_account_and_history_denied(self):
        self.r.decide('admin', 'alice', 'approved')
        self.r.decide('admin', 'bob', 'approved')
        self.r.link_account('admin', 'alice', 'a', 'alice_handle')
        with self.assertRaises(Denied):
            self.r.request('bob', 'a')
        with self.assertRaises(Denied):
            self.r.history('bob', 'alice')

    def test_manual_post_requires_ready_and_owner(self):
        self.r.decide('admin', 'alice', 'approved')
        self.r.decide('admin', 'bob', 'approved')
        self.r.link_account('admin', 'alice', 'a', 'alice_handle')
        job = self.r.request('alice', 'a')
        with self.assertRaises(Denied):
            self.r.review('alice', job, 'posted', 'https://www.tiktok.com/@alice/video/123')
        self.r.set_generation_result('admin', job, 'ready', 'approved-artifact-reference')
        with self.assertRaises(Denied):
            self.r.review('bob', job, 'posted', 'https://www.tiktok.com/@alice/video/123')
        self.r.review('alice', job, 'posted', 'https://www.tiktok.com/@alice/video/123')
        self.assertEqual(self.r.history('alice')[0][2], 'posted')

    def test_suspension_revokes_access(self):
        self.r.decide('admin', 'alice', 'approved')
        self.r.decide('admin', 'alice', 'suspended')
        with self.assertRaises(Denied):
            self.r.history('alice')

    def test_no_second_admin_bootstrap(self):
        with self.assertRaises(Denied):
            self.r.bootstrap_admin('other', 'other@example.test')


if __name__ == '__main__':
    unittest.main()
