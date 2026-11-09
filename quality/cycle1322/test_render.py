import unittest
from render import SCENES
class TestScenes(unittest.TestCase):
 def test_five_scenes(self): self.assertEqual(len(SCENES),5)
 def test_no_private_assets(self): self.assertTrue(all('IMG_' not in str(s) for s in SCENES))
if __name__=='__main__': unittest.main()
