import unittest
from tenant_core import Actor, AccessDenied, Status, TenantRegistry

class TenantTests(unittest.TestCase):
    def setUp(self):
        self.db = TenantRegistry()
        self.root = Actor('root', None, 'platform_admin', True)
        self.a = self.db.create_customer(self.root)
        self.b = self.db.create_customer(self.root)
        self.db.set_status(self.root, self.a, Status.ACTIVE)
        self.db.set_status(self.root, self.b, Status.ACTIVE)
        self.alice = Actor('alice', self.a, 'customer_admin', True)
        self.bob = Actor('bob', self.b, 'customer_admin', True)
        self.db.link_account(self.alice, self.a, 'account-a')
        self.db.link_account(self.bob, self.b, 'account-b')

    def test_cross_tenant_read_and_write_denied(self):
        job = self.db.submit_job(self.bob, self.b, 'account-b')
        with self.assertRaises(AccessDenied):
            self.db.get_job(self.alice, self.a, job)
        with self.assertRaises(AccessDenied):
            self.db.link_account(self.alice, self.b, 'hijack')
        with self.assertRaises(AccessDenied):
            self.db.usage(self.alice, self.b)

    def test_unapproved_denied(self):
        with self.assertRaises(AccessDenied):
            self.db.submit_job(Actor('stranger', self.a, 'employee', False), self.a, 'account-a')

    def test_suspended_denied(self):
        self.db.set_status(self.root, self.a, Status.SUSPENDED)
        with self.assertRaises(AccessDenied):
            self.db.submit_job(self.alice, self.a, 'account-a')

    def test_usage_isolated(self):
        self.db.submit_job(self.alice, self.a, 'account-a', 2.5)
        self.db.submit_job(self.alice, self.a, 'account-a', 1.25)
        self.db.submit_job(self.bob, self.b, 'account-b', 9)
        self.assertEqual(self.db.usage(self.alice, self.a), {'jobs': 2, 'estimated_cost': 3.75})
        self.assertEqual(self.db.usage(self.bob, self.b), {'jobs': 1, 'estimated_cost': 9})

    def test_failed_job_does_not_mutate_other_customer(self):
        before = self.db.usage(self.bob, self.b)
        with self.assertRaises(AccessDenied):
            self.db.submit_job(self.alice, self.a, 'account-b')
        self.assertEqual(before, self.db.usage(self.bob, self.b))

if __name__ == '__main__':
    unittest.main()
