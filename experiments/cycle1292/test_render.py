import unittest
from pathlib import Path
from render import SCENES
class ReviewContract(unittest.TestCase):
    def test_four_scenes(self): self.assertEqual(len(SCENES),4)
    def test_no_publish_claim(self):
        source=Path(__file__).with_name('render.py').read_text()
        self.assertIn('REVIEW_ONLY',source)
        self.assertIn('audio absent',source)
if __name__=='__main__': unittest.main()
