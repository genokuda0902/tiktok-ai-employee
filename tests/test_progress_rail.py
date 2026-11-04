import unittest
from progress_rail import filtergraph
class TestProgressRail(unittest.TestCase):
    def test_duration(self): self.assertIn("t/23.033",filtergraph())
    def test_safe_top(self): self.assertIn("y=250",filtergraph())
    def test_width(self): self.assertIn("900*min",filtergraph())
if __name__=="__main__": unittest.main()
