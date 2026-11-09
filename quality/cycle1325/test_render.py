import unittest
from render import SCENES
class RenderTest(unittest.TestCase):
 def test_scenes(self): self.assertEqual(len(SCENES),4)
 def test_captions(self): self.assertTrue(all(a and b for a,b in SCENES))
 def test_no_personal_data(self): self.assertTrue(all('@' not in a+b for a,b in SCENES))
if __name__=='__main__': unittest.main()
