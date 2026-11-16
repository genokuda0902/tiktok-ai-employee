import unittest
from render import filtergraph
class TestDrift(unittest.TestCase):
 def test_default(self):
  self.assertIn('scale=1080:1920',filtergraph())
 def test_zero(self):
  self.assertEqual(filtergraph(margin=0),'null')
 def test_invalid(self):
  with self.assertRaises(ValueError):filtergraph(margin=40)
if __name__=='__main__': unittest.main()
