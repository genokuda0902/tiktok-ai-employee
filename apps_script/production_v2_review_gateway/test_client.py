import hashlib
import hmac
import unittest
from unittest.mock import patch

from client import EXPECTED_SHA256, EXPECTED_NAME, build_payload


class TestPinnedGatewayClient(unittest.TestCase):
    def test_wrong_bytes_rejected(self):
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            build_payload(b'old fixed video', 'test-secret')

    def test_empty_secret_rejected(self):
        with self.assertRaisesRegex(ValueError, 'secret missing'):
            build_payload(b'x', '')

    def test_signature_canonical_matches_gas_protocol(self):
        # Isolate protocol framing without pretending fixture bytes are the MP4.
        test_digest = hashlib.sha256(b'test-only').hexdigest()
        with patch('client.EXPECTED_SHA256', test_digest):
            result = build_payload(b'test-only', 'test-secret', 123456)
        canonical = '\n'.join(('123456', EXPECTED_NAME, test_digest,
                               result['content_b64'])).encode()
        self.assertEqual(result['signature'], hmac.new(b'test-secret', canonical,
                                                    hashlib.sha256).hexdigest())


if __name__ == '__main__':
    unittest.main()
