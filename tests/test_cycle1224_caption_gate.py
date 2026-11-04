import unittest
from quality.cycle1224_caption_gate import validate_cues, audit_manifest


class SubtitleGateTests(unittest.TestCase):
    def test_valid_structural_cues(self):
        self.assertEqual(validate_cues([{"start": 0, "end": 1, "text": "目的"}], 3), [])

    def test_reject_overlap(self):
        self.assertTrue(validate_cues([{"start": 0, "end": 2, "text": "A"}, {"start": 1, "end": 3, "text": "B"}], 4))

    def test_reject_empty_and_out_of_bounds(self):
        self.assertTrue(validate_cues([{"start": 0, "end": 5, "text": ""}], 3))

    def test_fail_closed_without_human_review(self):
        result = audit_manifest({"duration": 3, "cues": [{"start": 0, "end": 1, "text": "目的"}]})
        self.assertFalse(result["passed"])
        self.assertFalse(result["publication_approved"])


if __name__ == "__main__":
    unittest.main()
