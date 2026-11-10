import unittest
from storyboard_gate import Scene, validate_storyboard

class TestStoryboard(unittest.TestCase):
    def setUp(self):
        self.scenes = [Scene(2.5, "課題", "表"), Scene(2.5, "操作", "式"), Scene(2.5, "結果", "合計"), Scene(2.5, "保存", "まとめ")]
    def test_review_only_without_narration(self):
        r = validate_storyboard(self.scenes)
        self.assertFalse(r["posting_allowed"])
        self.assertIn("japanese_narration_unverified", r["issues"])
    def test_reject_empty_visual(self):
        s = list(self.scenes)
        s[1] = Scene(2.5, "操作", "")
        self.assertIn("invalid_scene", validate_storyboard(s)["issues"])
    def test_full_evidence(self):
        r = validate_storyboard(self.scenes, True, True, True)
        self.assertTrue(r["posting_allowed"])

if __name__ == "__main__": unittest.main()
