import unittest
from pathlib import Path
import importlib.util
p=Path(__file__).with_name('render.py')
spec=importlib.util.spec_from_file_location('cycle1633',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestReview(unittest.TestCase):
    def test_four_scenes(self): self.assertEqual(len(m.SCENES),4)
    def test_1080_vertical(self): self.assertEqual((m.W,m.H),(1080,1920))
    def test_no_personal_data(self): self.assertTrue(all('株式会社ABC' not in s[0] for s in m.SCENES))
    def test_review_only(self): self.assertNotIn('upload',Path(p).read_text().lower())
if __name__=='__main__': unittest.main()
