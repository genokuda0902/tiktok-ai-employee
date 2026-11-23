import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
import json
from tools.delivery_integrity import inspect

class DeliveryIntegrityTests(unittest.TestCase):
    @patch("tools.delivery_integrity.subprocess.check_output")
    def test_matching_1080p_still_not_approved(self, probe):
        probe.return_value = json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920,"codec_name":"h264"},{"codec_type":"audio","codec_name":"aac"}]})
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"test.mp4"; p.write_bytes(b"fixture")
            import hashlib
            r = inspect(p, hashlib.sha256(b"fixture").hexdigest())
            self.assertTrue(r["delivery_verified"])
            self.assertFalse(r["posting_allowed"])
            self.assertFalse(r["japanese_narration_verified"])

    @patch("tools.delivery_integrity.subprocess.check_output")
    def test_wrong_resolution_and_hash_fail(self, probe):
        probe.return_value = json.dumps({"streams":[{"codec_type":"video","width":512,"height":910}]})
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"test.mp4"; p.write_bytes(b"fixture")
            r = inspect(p, "0"*64)
            self.assertFalse(r["delivery_verified"])
            self.assertFalse(r["resolution_ok"])
            self.assertFalse(r["checksum_match"])
