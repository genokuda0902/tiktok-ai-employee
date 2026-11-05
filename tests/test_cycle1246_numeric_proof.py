import unittest
from cycle1246_numeric_proof import SCENES
class TestStory(unittest.TestCase):
    def test_stages(self): self.assertEqual([s[0] for s in SCENES],["BEFORE","ACTION","AFTER"])
    def test_sum(self): self.assertIn("SUM(B2:B3)",SCENES[1][2]);self.assertIn("300",SCENES[2][3])
if __name__=="__main__":unittest.main()
