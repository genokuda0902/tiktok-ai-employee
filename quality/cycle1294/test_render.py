import unittest
from pathlib import Path
import importlib.util
p=Path(__file__).with_name('render.py')
spec=importlib.util.spec_from_file_location('cycle1294_render',p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class Contract(unittest.TestCase):
    def test_four_scenes(self):
        self.assertEqual(len(mod.SCENES),4)
    def test_japanese_and_original_text(self):
        self.assertTrue(all(all((a,b,c)) for a,b,c in mod.SCENES))
    def test_review_only(self):
        self.assertIn('REVIEW ONLY',p.read_text(encoding='utf-8'))
    def test_no_auto_post(self):
        self.assertNotIn('tiktok.upload',p.read_text(encoding='utf-8'))
if __name__=='__main__': unittest.main()
