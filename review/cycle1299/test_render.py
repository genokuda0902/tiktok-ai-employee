import unittest
from pathlib import Path
import importlib.util
p=Path(__file__).with_name('render.py')
s=importlib.util.spec_from_file_location('cycle1299_render',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestReview(unittest.TestCase):
 def test_four_scenes(self): self.assertEqual(len(m.SCENES),4)
 def test_no_private_assets(self): self.assertNotIn('IMG_5805',p.read_text())
 def test_no_autopost(self): self.assertNotIn('tiktok_api',p.read_text())
 def test_review_only(self): self.assertIn('-an',p.read_text())
if __name__=='__main__':unittest.main()
