import unittest
from pathlib import Path
from render import SCENES
class Contract(unittest.TestCase):
    def test_four_scenes(self): self.assertEqual(len(SCENES),4)
    def test_no_private_assets(self): self.assertTrue(all(isinstance(x,str) and x for scene in SCENES for x in scene))
    def test_narration_not_claimed(self): self.assertFalse(any("ナレーション済" in x for scene in SCENES for x in scene))
if __name__=="__main__": unittest.main()
