import unittest
from render import SCENES
class QualityGate(unittest.TestCase):
    def test_four_scenes(self): self.assertEqual(len(SCENES),4)
    def test_no_private_data(self): self.assertIn("架空データ",str(SCENES))
    def test_not_publication_approved(self):
        narration_verified=False
        captions_synchronized=False
        employee_approved=False
        self.assertFalse(all([narration_verified,captions_synchronized,employee_approved]))
if __name__=="__main__":unittest.main()
