import unittest
from caption_qa import assess
class QATests(unittest.TestCase):
 def test_missing_audio_blocks(self):
  x=assess(dict(caption_font_px=48,caption_contrast_border=True,assets_approved=True,employee_approved=True))
  self.assertFalse(x["publication_approved"])
  self.assertIn("japanese_narration_missing",x["issues"])
 def test_small_text_blocks(self):
  self.assertIn("caption_too_small_at_1080p",assess({"caption_font_px":30})["issues"])
 def test_full_approval_required(self):
  x=dict(caption_font_px=48,caption_contrast_border=True,japanese_narration_verified=True,speech_sync_verified=True,assets_approved=True,employee_approved=True)
  self.assertTrue(assess(x)["publication_approved"])
if __name__=="__main__": unittest.main()
