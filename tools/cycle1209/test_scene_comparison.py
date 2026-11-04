import unittest
from scene_comparison import filtergraph

class ComparisonTest(unittest.TestCase):
    def test_invalid_interval(self):
        for a,b in [(0,0),(5,2),(-1,2)]:
            with self.assertRaises(ValueError):
                filtergraph(a,b)
    def test_disclosure(self):
        s=filtergraph()
        self.assertIn("実績ではありません",s)
        self.assertIn("BEFORE",s)
        self.assertIn("AFTER",s)
    def test_interval(self):
        self.assertIn(r"between(t\,2\,4)",filtergraph(2,4))

if __name__=="__main__":
    unittest.main()
