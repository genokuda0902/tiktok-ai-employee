import unittest

from video_engine.quality.proof_density import validate_proof_sequence


class ProofDensityTests(unittest.TestCase):
    def test_valid_sequence(self):
        ok, errors = validate_proof_sequence([
            {"phase": "INPUT"},
            {"phase": "TRANSFORM"},
            {"phase": "RESULT", "comparison": True, "publication": "HUMAN_REVIEW"},
        ])
        self.assertTrue(ok)
        self.assertEqual([], errors)

    def test_missing_transform_fails(self):
        ok, errors = validate_proof_sequence([
            {"phase": "INPUT"},
            {"phase": "RESULT", "comparison": True},
        ])
        self.assertFalse(ok)
        self.assertIn("missing_transform", errors)

    def test_wrong_order_fails(self):
        ok, errors = validate_proof_sequence([
            {"phase": "RESULT", "comparison": True},
            {"phase": "INPUT"},
            {"phase": "TRANSFORM"},
        ])
        self.assertFalse(ok)
        self.assertIn("proof_order_invalid", errors)

    def test_result_requires_comparison(self):
        ok, errors = validate_proof_sequence([
            {"phase": "INPUT"},
            {"phase": "TRANSFORM"},
            {"phase": "RESULT"},
        ])
        self.assertFalse(ok)
        self.assertIn("result_comparison_missing", errors)

    def test_auto_post_and_publication_approval_fail_closed(self):
        ok, errors = validate_proof_sequence([
            {"phase": "INPUT"},
            {"phase": "TRANSFORM", "auto_post": True},
            {"phase": "RESULT", "comparison": True, "publication": "APPROVED"},
        ])
        self.assertFalse(ok)
        self.assertIn("auto_post_forbidden", errors)
        self.assertIn("publication_must_require_human_review", errors)


if __name__ == "__main__":
    unittest.main()
