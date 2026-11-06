import unittest
from pathlib import Path
import importlib.util
p=Path(__file__).with_name('render.py')
spec=importlib.util.spec_from_file_location('cycle1271',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestReview(unittest.TestCase):
    def test_three_scenes(self): self.assertEqual(len(m.SCENES),3)
    def test_no_publication_claim(self): self.assertIn('REVIEW ONLY',p.read_text())
    def test_review_only_narration(self): self.assertIn('NO narration',p.read_text())
if __name__=='__main__': unittest.main()
