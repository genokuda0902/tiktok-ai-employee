import unittest
from cycle874.chart_truth import GENRES
from cycle877.chart_reveal import (COUNT,REVEAL_FRAMES,POLICY,bar_heights,
    bar_state,render_frame,revealed_groups)
from cycle877.audio_caption_audit import CAPTION_WINDOWS,active_mask
import numpy as np

class ChartRevealTests(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(GENRES),10)
 def test_group_reveal_sequence(self):
  self.assertEqual(revealed_groups(0),())
  self.assertEqual(revealed_groups(9),(0,))
  self.assertEqual(revealed_groups(26),(0,1))
  self.assertEqual(revealed_groups(43),(0,1,2))
 def test_reveal_never_partial_for_all_frames_and_genres(self):
  for genre,g in GENRES.items():
   ah,bh=bar_heights(g)
   for i in range(COUNT):
    for j,state in enumerate(bar_state(i,genre)):
     self.assertEqual(state['a_height'],ah[j])
     self.assertEqual(state['b_height'],bh[j])
     self.assertEqual((state['a'],state['b']),(g.a[j],g.b[j]))
 def test_final_ranking(self):
  g=GENRES['ai_work']
  self.assertEqual(g.a,(12,16,18));self.assertEqual(g.b,(8,9,12))
  self.assertGreater(bar_heights(g)[0][2],bar_heights(g)[0][1])
 def test_height_proportional(self):
  for g in GENRES.values():
   ah,bh=bar_heights(g)
   for x,y in zip(g.a,ah):self.assertLess(abs(y-270*x/max(*g.a,*g.b)),.51)
   for x,y in zip(g.b,bh):self.assertLess(abs(y-270*x/max(*g.a,*g.b)),.51)
 def test_text_renders_all_genres(self):
  for genre in GENRES:
   im=render_frame(50,genre)
   self.assertEqual(im.size,(1080,960))
 def test_edge_frames(self):
  self.assertEqual(render_frame(0).size,(1080,960))
  self.assertEqual(render_frame(80).size,(1080,960))
 def test_invalid_frame(self):
  with self.assertRaises(ValueError):revealed_groups(81)
 def test_policy_fail_closed(self):
  self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['external_upload'])
 def test_caption_windows_valid(self):
  self.assertEqual(len(CAPTION_WINDOWS),8)
  self.assertTrue(all(0<=s<e<=23.04 for s,e in CAPTION_WINDOWS))
 def test_silence_and_tone(self):
  a=np.zeros(16000);a[4000:8000]=0.25*np.sin(np.arange(4000)*2*np.pi*440/16000)
  m=active_mask(a)
  self.assertFalse(m[0]);self.assertTrue(m[20]);self.assertFalse(m[-1])
 def test_reject_empty_audio(self):
  with self.assertRaises(ValueError):active_mask(np.zeros(1))

if __name__=='__main__':unittest.main()
