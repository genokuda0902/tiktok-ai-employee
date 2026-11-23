import unittest
from render import SCENES
class TestContract(unittest.TestCase):
    def test_four_scenes(self): self.assertEqual(len(SCENES),4)
    def test_review_only(self): self.assertFalse(any("投稿承認済" in " ".join(s) for s in SCENES))
    def test_story_order(self): self.assertEqual([s[0][:2] for s in SCENES],["01","02","03","04"])
    def test_fictional(self): self.assertIn("架空", " ".join(SCENES[2]))
if __name__=="__main__":unittest.main()
