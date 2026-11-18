import unittest
from render import filtergraph
class RenderTest(unittest.TestCase):
 def test_hook_window(self): self.assertIn("lt(t,1.5)",filtergraph())
 def test_progress(self): self.assertIn("min(t/12,1)",filtergraph())
 def test_review_watermark(self): self.assertIn("REVIEW ONLY",filtergraph())
 def test_reject_invalid_duration(self):
  with self.assertRaises(ValueError): filtergraph(0)
if __name__=='__main__': unittest.main()
