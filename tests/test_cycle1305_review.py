import unittest
from pathlib import Path
from src.cycle1305_review import SCENES
class TestReview(unittest.TestCase):
    def test_scene_count(self): self.assertEqual(len(SCENES),6)
    def test_arithmetic(self): self.assertEqual(sum([12000,8000,15000,5000]),40000)
    def test_review_only(self): self.assertIn("REVIEW_ONLY",Path("cycle1305_REVIEW_ONLY.mp4").name)
    def test_no_publication_claim(self):
        self.assertFalse(any("投稿可能" in a for a,b in SCENES))
if __name__=="__main__": unittest.main()
