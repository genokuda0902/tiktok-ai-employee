import json
import unittest

from scripts.drive_review_artifact_handoff import (
    _credential_kind,
    _drive_error_reason,
    _validate_destination,
)


class DriveReviewAuthTests(unittest.TestCase):
    def test_service_account_is_supported(self):
        self.assertEqual(
            _credential_kind({'type': 'service_account'}), 'service_account')

    def test_authorized_user_is_supported(self):
        self.assertEqual(
            _credential_kind({'type': 'authorized_user'}), 'authorized_user')

    def test_unknown_credential_type_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, 'service_account or authorized_user'):
            _credential_kind({'type': 'external_account'})

    def test_quota_reason_is_extracted_without_full_error(self):
        class Error(Exception):
            content = json.dumps({
                'error': {'errors': [{'reason': 'storageQuotaExceeded'}]}
            }).encode()

        self.assertEqual(_drive_error_reason(Error()), 'storageQuotaExceeded')

    def test_malformed_error_has_no_reason(self):
        class Error(Exception):
            content = b'not-json'

        self.assertIsNone(_drive_error_reason(Error()))

    def test_service_account_my_drive_is_blocked_before_upload(self):
        folder = {
            'mimeType': 'application/vnd.google-apps.folder',
            'capabilities': {'canAddChildren': True},
            'permissions': [{'type': 'user', 'role': 'writer'}],
        }
        with self.assertRaisesRegex(RuntimeError, 'cannot store files in My Drive'):
            _validate_destination(folder, 'service_account')

    def test_authorized_user_my_drive_is_allowed(self):
        folder = {
            'mimeType': 'application/vnd.google-apps.folder',
            'capabilities': {'canAddChildren': True},
            'permissions': [{'type': 'user', 'role': 'owner'}],
        }
        self.assertIsNone(_validate_destination(folder, 'authorized_user'))

    def test_workspace_shared_drive_is_allowed_for_service_account(self):
        folder = {
            'mimeType': 'application/vnd.google-apps.folder',
            'driveId': 'shared-drive-id',
            'capabilities': {'canAddChildren': True},
            'permissions': [{'type': 'group', 'role': 'writer'}],
        }
        self.assertIsNone(_validate_destination(folder, 'service_account'))

    def test_public_destination_is_blocked(self):
        folder = {
            'mimeType': 'application/vnd.google-apps.folder',
            'capabilities': {'canAddChildren': True},
            'permissions': [{'type': 'anyone', 'role': 'reader'}],
        }
        with self.assertRaisesRegex(RuntimeError, 'public/domain'):
            _validate_destination(folder, 'authorized_user')


if __name__ == '__main__':
    unittest.main()
