import unittest
from render import SCENES
class TestRender(unittest.TestCase):
 def test_three_scenes(self): self.assertEqual(len(SCENES),3)
 def test_japanese(self): self.assertTrue(all(any(ord(c)>127 for c in a+b) for a,b in SCENES))
 def test_no_fake_voice(self):
  import inspect,render
  self.assertIn("'-an'",inspect.getsource(render.render))
if __name__=='__main__': unittest.main()
