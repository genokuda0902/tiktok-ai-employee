import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from quality_cycle472.evidence_gate import generate_evidence, validate_review_manifest

REVIEW = {
    "rights": "ORIGINAL_SYNTHETIC", "privacy": "NO_REAL_PERSONAL_DATA",
    "human_approved": False, "publication": "NOT_APPROVED",
    "narration_verified": False, "captions_synced": False, "auto_post": False,
}

class Cycle472EvidenceTests(unittest.TestCase):
    def test_real_python_execution(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "evidence.json"
            result = generate_evidence(path)
            self.assertEqual(result["observed_stdout"], "35")
            self.assertEqual(json.loads(path.read_text())["source"], "LOCAL_PYTHON_EXECUTION")

    def test_mismatch_is_fatal(self):
        with tempfile.TemporaryDirectory() as d:
            with patch("quality_cycle472.evidence_gate.subprocess.check_output", return_value="36\n"):
                with self.assertRaisesRegex(RuntimeError, "FAIL CLOSED"):
                    generate_evidence(Path(d) / "evidence.json")

    def test_review_only_gate(self):
        validate_review_manifest(REVIEW)

    def test_reject_false_narration_claim(self):
        with self.assertRaisesRegex(ValueError, "narration"):
            validate_review_manifest({**REVIEW, "narration_verified": True})

    def test_reject_false_sync_claim(self):
        with self.assertRaisesRegex(ValueError, "sync"):
            validate_review_manifest({**REVIEW, "captions_synced": True})

    def test_reject_unauthorized_rights(self):
        with self.assertRaisesRegex(ValueError, "rights"):
            validate_review_manifest({**REVIEW, "rights": "UNKNOWN"})

    def test_reject_auto_post(self):
        with self.assertRaisesRegex(ValueError, "posting"):
            validate_review_manifest({**REVIEW, "auto_post": True})

if __name__ == "__main__":
    unittest.main()
