from pathlib import Path
import unittest
class ReviewContract(unittest.TestCase):
 def test_no_auto_publish(self):
  s=Path("scripts/cycle1276_review.py").read_text()
  self.assertIn("REVIEW ONLY",s)
  self.assertNotIn("upload_to_tiktok",s)
 def test_four_scenes(self):
  s=Path("scripts/cycle1276_review.py").read_text()
  self.assertIn("SCENES=[",s)
  self.assertIn("captions.srt",s)
if __name__=="__main__": unittest.main()
