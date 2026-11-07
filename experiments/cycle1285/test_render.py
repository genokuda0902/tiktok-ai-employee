import unittest
from render import SCENES
class TestRenderer(unittest.TestCase):
    def test_four_scenes(self): self.assertEqual(len(SCENES),4)
    def test_unique_titles(self): self.assertEqual(len(set(x[0] for x in SCENES)),4)
    def test_no_publication_approval(self):
        self.assertNotIn("publication_approved=True",open(__file__,encoding="utf-8").read())
if __name__=="__main__": unittest.main()
