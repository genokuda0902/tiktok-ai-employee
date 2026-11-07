import unittest
from quality.cycle1278_gate import publishable
class GateTest(unittest.TestCase):
 def test_silent_rejected(self):
  self.assertFalse(publishable({"video":True,"audio":False,"resolution":[1080,1920]},True,True,True))
 def test_unapproved_rejected(self):
  self.assertFalse(publishable({"video":True,"audio":True,"resolution":[1080,1920]},False,True,True))
 def test_complete_gate(self):
  self.assertTrue(publishable({"video":True,"audio":True,"resolution":[1080,1920]},True,True,True))
if __name__=="__main__":unittest.main()
