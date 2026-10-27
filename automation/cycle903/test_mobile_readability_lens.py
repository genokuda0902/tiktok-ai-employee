import unittest
from mobile_readability_lens import GENRES,PHASES,ROI,CARD,CAPTION_TOP,RELEASE,validate,ffmpeg_filter
class TestMobileLens(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for g in GENRES:self.assertTrue(validate(g))
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):validate("unknown")
 def test_three_stages(self):self.assertEqual(len(PHASES),3)
 def test_caption_safe(self):
  self.assertLess(CARD[3],CAPTION_TOP)
  for _,_,_,bottom in ROI:self.assertLess(bottom,CAPTION_TOP)
 def test_audio_unmodified_by_filter(self):
  self.assertNotIn("volume",ffmpeg_filter("/font","/tmp"))
 def test_no_publish(self):self.assertFalse(any(RELEASE.values()))
 def test_has_three_distinct_phases(self):
  self.assertIn("17.4",ffmpeg_filter("/font","/tmp"))
  self.assertIn("20.3",ffmpeg_filter("/font","/tmp"))
 def test_overlay_textfiles(self):self.assertIn("stage_2_detail.txt",ffmpeg_filter("/font","/tmp"))
if __name__=="__main__":unittest.main()
