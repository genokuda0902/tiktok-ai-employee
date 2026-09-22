import hashlib
import hmac
import os
import unittest
from unittest import mock

from scripts.drive_review_gateway_client import (
    EXPECTED,
    NAME,
    _canonical,
    build_payload,
    send,
)


class DriveReviewGatewayClientTests(unittest.TestCase):
    def setUp(self):
        self.env = mock.patch.dict(os.environ, {'EXPECTED_SHA256': EXPECTED})
        self.env.start()

    def tearDown(self):
        self.env.stop()

    @mock.patch('scripts.drive_review_gateway_client._digest', return_value=EXPECTED)
    def test_payload_is_short_lived_and_hmac_signed(self, _fake_digest):
        payload = build_payload(b'video', 'secret-value', timestamp=123)
        expected = hmac.new(
            b'secret-value',
            _canonical(123, NAME, EXPECTED, payload['content_b64']),
            hashlib.sha256,
        ).hexdigest()
        self.assertEqual(payload['signature'], expected)
        self.assertEqual(payload['timestamp'], 123)
        self.assertNotIn('secret-value', str(payload))

    def test_empty_secret_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, 'secret missing'):
            build_payload(b'video', '', timestamp=123)

    def test_unpinned_hash_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, 'SHA-256 mismatch'):
            build_payload(b'wrong-video', 'secret-value', timestamp=123)

    def test_non_apps_script_url_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, 'invalid Apps Script'):
            send('/tmp/never-read', 'https://example.com/upload', 'secret-value')


if __name__ == '__main__':
    unittest.main()
