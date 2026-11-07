import unittest
from render import SCENES, W, H
class Contract(unittest.TestCase):
    def test_vertical(self): self.assertEqual((W,H),(1080,1920))
    def test_scenes(self): self.assertEqual(len(SCENES),4)
    def test_text(self): self.assertTrue(all(a and b for a,b in SCENES))
    def test_review_only(self):
        import inspect,render
        self.assertIn('NOT FOR POSTING',inspect.getsource(render.make_image))
if __name__=='__main__': unittest.main()
