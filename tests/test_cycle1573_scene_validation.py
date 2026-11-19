import unittest
from quality.cycle1573_scene_validation import Scene, validate_scenes, publication_allowed

class SceneValidationTest(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_scenes([Scene(0, 3, "導入"), Scene(3, 6, "比較")], 6))
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            validate_scenes([Scene(0, 3, "A"), Scene(2, 6, "B")], 6)
    def test_no_approval_without_audio(self):
        self.assertFalse(publication_allowed(captions_synced=True, assets_approved=True, employee_approved=True))
    def test_all_evidence(self):
        self.assertTrue(publication_allowed(narration_verified=True, captions_synced=True, assets_approved=True, employee_approved=True))
if __name__ == "__main__":
    unittest.main()
