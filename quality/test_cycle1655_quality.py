import unittest
from cycle1655_quality import validate_scenes, posting_allowed

class QualityTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_scenes([{"start":0,"end":3,"caption":"入力を整理"},{"start":3,"end":6,"caption":"表記を統一"}]))
    def test_overlap(self):
        with self.assertRaises(ValueError):
            validate_scenes([{"start":0,"end":4,"caption":"A"},{"start":3,"end":6,"caption":"B"}])
    def test_long_caption(self):
        with self.assertRaises(ValueError):
            validate_scenes([{"start":0,"end":3,"caption":"あ"*33}])
    def test_fail_closed(self):
        self.assertFalse(posting_allowed(narration_verified=False,captions_synced=True,assets_approved=True,employee_approved=True))

if __name__ == "__main__": unittest.main()
