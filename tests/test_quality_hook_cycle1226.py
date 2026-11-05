import unittest
from src.quality_hook_cycle1226 import filtergraph
class HookTests(unittest.TestCase):
    def test_window(self): self.assertIn("between(t,0.3,3.3)",filtergraph())
    def test_hook(self): self.assertIn("3つの確認",filtergraph())
    def test_invalid(self):
        with self.assertRaises(ValueError): filtergraph(4,2)
if __name__=="__main__": unittest.main()
