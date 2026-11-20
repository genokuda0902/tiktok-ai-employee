import unittest
from render import SCENES
class ReviewContract(unittest.TestCase):
 def test_six_scenes(self): self.assertEqual(len(SCENES),6)
 def test_public_safe_sample(self): self.assertIn("架空",str(SCENES))
 def test_review_only_not_approved(self): self.assertNotIn("PUBLICATION_APPROVED",str(SCENES))
if __name__=="__main__":unittest.main()
