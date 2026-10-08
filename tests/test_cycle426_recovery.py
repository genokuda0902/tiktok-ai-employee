import unittest
from pathlib import Path
class Cycle426Checks(unittest.TestCase):
 def test_patch_script_present(self):
  self.assertTrue(Path('src/cycle426_patch.py').is_file())
 def test_no_auto_post(self):
  s=Path('quality/cycle426_status.json').read_text()
  self.assertIn('"auto_post": false',s)
 def test_review_only(self):
  s=Path('quality/cycle426_status.json').read_text()
  self.assertIn('HUMAN_REVIEW',s)
if __name__=='__main__': unittest.main()
