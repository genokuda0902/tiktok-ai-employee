import unittest
from dataclasses import replace
from chart_truth import GENRES,COUNT,POLICY,bar_heights,draw_frame,ease,validate_genre,render
class ChartTruthTests(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for k in GENRES:
   with self.subTest(k=k):self.assertEqual(validate_genre(k),GENRES[k])
 def test_ai_work_fictional_source(self):
  g=GENRES['ai_work'];self.assertEqual(g.a,(12,16,18));self.assertEqual(g.b,(8,9,12))
 def test_june_bar_is_tallest(self):
  a,b=bar_heights(GENRES['ai_work']);self.assertGreater(a[2],a[1]);self.assertGreater(b[2],b[1])
 def test_common_axis_ratio(self):
  a,b=bar_heights(GENRES['ai_work']);self.assertEqual(a[2],260);self.assertEqual(b[2],round(260*12/18))
 def test_all_genres_positive_values(self):
  for g in GENRES.values():self.assertTrue(all(x>0 for x in (*g.a,*g.b)))
 def test_animation_progress_monotone(self):
  self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1)
  self.assertTrue(all(ease(i/30)<=ease((i+1)/30) for i in range(30)))
 def test_frame_dimensions(self):self.assertEqual(draw_frame(30).size,(1080,960))
 def test_scene_changes_over_time(self):self.assertNotEqual(draw_frame(1).tobytes(),draw_frame(75).tobytes())
 def test_safe_picture_region_only(self):self.assertEqual(1245-285,draw_frame(0).height)
 def test_bad_genre_rejected(self):
  with self.assertRaises(ValueError):validate_genre('private')
 def test_frame_range_rejected(self):
  for n in (-1,COUNT):
   with self.assertRaises(ValueError):draw_frame(n)
 def test_missing_source_fails_closed(self):
  with self.assertRaises(FileNotFoundError):render('/does/not/exist.mp4','/tmp/not-made.mp4',{})
 def test_bad_manifest_fails_closed(self):
  import tempfile
  from pathlib import Path
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'fake.mp4';src.write_bytes(b'private')
   with self.assertRaises(ValueError):render(src,Path(d)/'out.mp4',{'source_sha256':'wrong'})
 def test_policy_disallows_release(self):
  self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['automatic_posting']);self.assertFalse(POLICY['external_upload'])
 def test_bad_values_rejected(self):
  original=GENRES['ai_work']
  try:
   GENRES['ai_work']=replace(original,a=(12,16,-1))
   with self.assertRaises(ValueError):validate_genre('ai_work')
  finally:GENRES['ai_work']=original
 def test_bar_heights_derived_from_values(self):
  for g in GENRES.values():
   a,b=bar_heights(g);self.assertEqual(max((*a,*b)),260)
   self.assertTrue(all(0<v<=260 for v in (*a,*b)))
if __name__=='__main__':unittest.main()
