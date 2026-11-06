import unittest
from render import SCENES
class TestScenes(unittest.TestCase):
    def test_three_scenes(self): self.assertEqual(len(SCENES),3)
    def test_no_empty_caption(self): self.assertTrue(all(all(s.strip() for s in scene) for scene in SCENES))
if __name__=='__main__': unittest.main()
