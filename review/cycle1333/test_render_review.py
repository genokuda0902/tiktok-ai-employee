import unittest
from render_review import SCENES
class TestScenes(unittest.TestCase):
    def test_five_scenes(self): self.assertEqual(len(SCENES),5)
    def test_no_empty(self): self.assertTrue(all(a and b for a,b in SCENES))
    def test_synthetic_disclosure(self): self.assertIn("架空",SCENES[-1][1])
if __name__=="__main__":unittest.main()
