import unittest
from src.okuda_single_operator import TrustedIdentity, owner_principal
from src.manual_posting_flow import Forbidden


class OwnerGateTests(unittest.TestCase):
    def test_owner_is_admin_after_verified_authentication(self):
        principal = owner_principal(TrustedIdentity('owner-123', True, True), configured_owner_subject='owner-123')
        self.assertEqual(principal.user_id, 'owner-123')
        principal.require(admin=True)

    def test_unverified_issuer_rejected(self):
        with self.assertRaises(Forbidden):
            owner_principal(TrustedIdentity('owner-123', True, False), configured_owner_subject='owner-123')

    def test_unauthenticated_rejected(self):
        with self.assertRaises(Forbidden):
            owner_principal(TrustedIdentity('owner-123', False, True), configured_owner_subject='owner-123')

    def test_other_employee_rejected(self):
        with self.assertRaises(Forbidden):
            owner_principal(TrustedIdentity('employee-2', True, True), configured_owner_subject='owner-123')

    def test_missing_owner_configuration_rejected(self):
        with self.assertRaises(Forbidden):
            owner_principal(TrustedIdentity('owner-123', True, True), configured_owner_subject='')

    def test_empty_subject_rejected(self):
        with self.assertRaises(Forbidden):
            owner_principal(TrustedIdentity('', True, True), configured_owner_subject='owner-123')


if __name__ == '__main__':
    unittest.main()
