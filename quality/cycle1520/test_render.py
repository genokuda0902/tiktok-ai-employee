import unittest
from render import stage_at
class Stages(unittest.TestCase):
 def test_boundaries(self):
  self.assertEqual([stage_at(t) for t in (0,2,4,6,8)], [0,1,2,3,3])
 def test_no_negative(self):
  self.assertEqual(stage_at(-3),0)
if __name__=="__main__": unittest.main()
