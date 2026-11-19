import unittest
from quality.cycle1572_animation import Scene, validate_scenes, publication_allowed

class Cycle1572Tests(unittest.TestCase):
    def test_contiguous_scenes(self):
        self.assertTrue(validate_scenes([Scene("a","b",0,3),Scene("c","d",3,6)],6))
    def test_gap_rejected(self):
        with self.assertRaises(ValueError):
            validate_scenes([Scene("a","b",0,3),Scene("c","d",4,6)],6)
    def test_unapproved_rejected(self):
        self.assertFalse(publication_allowed(japanese_speech_verified=False,captions_synced=False,rights_approved=True,employee_approved=False))

if __name__ == "__main__":
    unittest.main()
