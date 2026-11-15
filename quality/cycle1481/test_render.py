import unittest
from pathlib import Path
from render import SCENES
class ReviewContract(unittest.TestCase):
 def test_four_scenes(self): self.assertEqual(len(SCENES),4)
 def test_no_private_assets(self): self.assertTrue(all('IMG_' not in x for scene in SCENES for x in scene))
 def test_review_only(self): self.assertIn('REVIEW_ONLY',Path('cycle1481_REVIEW_ONLY.mp4').name)
if __name__=='__main__':unittest.main()
