import unittest
from cycle878.caption_safe_area import (AI_WORK_LINES,CaptionCue,WINDOWS,default_cues,
  validate_cues,cue_at,make_card,make_background,filter_graph,TOP,HEIGHT,
  TEXT_RIGHT,TEXT_LEFT,POLICY)
from cycle874.chart_truth import GENRES

class CaptionSafetyTests(unittest.TestCase):
 def test_eight_original_sentence_cues(self):
  cues=default_cues();self.assertEqual(len(cues),8)
  self.assertEqual(cues[0].lines,AI_WORK_LINES[0]);self.assertTrue(validate_cues(cues))
 def test_nonoverlap_and_scene_windows(self):
  cues=default_cues()
  for i,c in enumerate(cues):
   self.assertEqual((c.start,c.end),WINDOWS[i])
   self.assertEqual(cue_at((c.start+c.end)/2,cues),i)
  self.assertIsNone(cue_at(3.05,cues))
 def test_reject_overlap(self):
  with self.assertRaises(ValueError):validate_cues((CaptionCue(0,2,('A','B')),CaptionCue(1,3,('C','D'))))
 def test_reject_short_hold(self):
  with self.assertRaises(ValueError):validate_cues((CaptionCue(0,.1,('A','B')),))
 def test_reject_long_text(self):
  with self.assertRaises(ValueError):validate_cues((CaptionCue(0,1,('あ'*25,'B')),))
 def test_reject_multiline(self):
  with self.assertRaises(ValueError):validate_cues((CaptionCue(0,1,('A\nB','C')),))
 def test_safe_zone(self):
  self.assertGreaterEqual(TEXT_LEFT,80)
  self.assertLessEqual(TEXT_RIGHT,865)
  self.assertLessEqual(TOP+HEIGHT,1840)
 def test_cards_fit_all_eight(self):
  for i,c in enumerate(default_cues()):
   self.assertEqual(make_card(c,i,8).size,(1080,HEIGHT))
 def test_background_opaque(self):
  b=make_background();self.assertEqual(b.getpixel((900,100))[3],255)
 def test_filter_graph_uses_windows(self):
  f=filter_graph(default_cues());self.assertIn('gte(t,0.27)*lt(t,2.93)',f)
  self.assertIn('fontsize=64',f)
 def test_ten_genre_reuse(self):
  self.assertEqual(len(GENRES),10)
  for key,g in GENRES.items():
   cue=CaptionCue(0,1,(g.headline,'結果を確認しよう。'))
   self.assertTrue(validate_cues((cue,)),key)
   self.assertEqual(make_card(cue,0,1).size,(1080,HEIGHT))
 def test_fail_closed_policy(self):
  self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['external_upload'])
  self.assertFalse(POLICY['automatic_posting'])

if __name__=='__main__':unittest.main()
