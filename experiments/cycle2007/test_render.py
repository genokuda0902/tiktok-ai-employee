import unittest
from render import filtergraph
class Tests(unittest.TestCase):
 def test_segments(self):
  f=filtergraph(); self.assertEqual(f.count('drawtext='),5);self.assertIn('between(t,18.100,22.625)',f)
 def test_invalid(self):
  with self.assertRaises(ValueError):filtergraph(0,22)
if __name__=='__main__':unittest.main()
