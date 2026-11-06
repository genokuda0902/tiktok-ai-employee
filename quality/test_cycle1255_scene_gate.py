import unittest
from cycle1255_scene_gate import Scene, check_scenes

class TestSceneGate(unittest.TestCase):
    def test_valid_but_not_publishable(self):
        r=check_scenes([Scene(0,3,"前"),Scene(3,6,"中"),Scene(6,9,"後")],9)
        self.assertTrue(r["timeline_valid"])
        self.assertFalse(r["publication_approved"])
        self.assertFalse(r["speech_synced_captions_verified"])
    def test_gap_rejected(self):
        with self.assertRaises(ValueError):
            check_scenes([Scene(0,3,"前"),Scene(4,9,"後")],9)
    def test_blank_caption_rejected(self):
        with self.assertRaises(ValueError):
            check_scenes([Scene(0,9," ")],9)
    def test_duration_rejected(self):
        with self.assertRaises(ValueError):
            check_scenes([Scene(0,8,"前")],9)
if __name__ == "__main__":
    unittest.main()
