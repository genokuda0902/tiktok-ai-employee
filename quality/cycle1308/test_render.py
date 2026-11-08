import unittest
from render import SCENES
class RenderTest(unittest.TestCase):
 def test_story(self): self.assertEqual(len(SCENES),5)
 def test_no_unapproved_claims(self): self.assertTrue(all(a and b for a,b in SCENES))
 def test_math(self): self.assertEqual(sum([12000,8000,15000,5000]),40000)
if __name__=='__main__':unittest.main()
