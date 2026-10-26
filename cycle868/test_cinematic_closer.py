import unittest
from pathlib import Path
from unittest.mock import patch
from cinematic_closer import GENRES, POLICY, draw_frame, ease, sha, W,H,FRAMES,START,COUNT,CAPTION_Y, render

class CinematicCloserTests(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(GENRES),10)
 def test_genres_unique(self):self.assertEqual(len(set(GENRES.values())),10)
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):draw_frame(1,'unknown')
 def test_invalid_frame_before(self):
  with self.assertRaises(ValueError):draw_frame(-1)
 def test_invalid_frame_after(self):
  with self.assertRaises(ValueError):draw_frame(COUNT)
 def test_frame_dimensions(self):self.assertEqual(draw_frame(0).size,(W,H))
 def test_safe_caption_region(self):self.assertEqual(132+H,CAPTION_Y)
 def test_full_timeline(self):self.assertEqual(START+COUNT,FRAMES)
 def test_no_unapproved_publication(self):
  for k in ('publication_approved','automatic_posting','external_upload','source_rights_reviewed'):self.assertFalse(POLICY[k])
 def test_explicit_review_only(self):self.assertTrue(POLICY['review_only'])
 def test_original_art(self):self.assertTrue(POLICY['original_procedural_art'])
 def test_ease_monotonic(self):self.assertEqual([ease(x) for x in (0,1)],[0,1])
 def test_genre_render(self):
  for genre in GENRES:self.assertEqual(draw_frame(48,genre).size,(W,H),genre)
 def test_different_stages(self):
  self.assertNotEqual(draw_frame(0).tobytes(),draw_frame(75).tobytes())
 def test_fail_closed_missing_source(self):
  with self.assertRaises(ValueError):render('/not/a/source.mp4','/tmp/cycle868.mp4',{},'ai_work')
 def test_fail_closed_unknown_genre(self):
  with self.assertRaises(ValueError):render('/not/a/source.mp4','/tmp/cycle868.mp4',{},'bad')
 def test_fail_closed_missing_manifest(self):
  import tempfile
  with tempfile.TemporaryDirectory() as tmp:
   src=Path(tmp)/'in.mp4';src.write_bytes(b'fake')
   with self.assertRaises(ValueError):render(src,Path(tmp)/'out.mp4',{},'ai_work')
 def test_fail_closed_same_file(self):
  import tempfile
  with tempfile.TemporaryDirectory() as tmp:
   src=Path(tmp)/'in.mp4';src.write_bytes(b'fake')
   with self.assertRaises(ValueError):render(src,src,{},'ai_work')

if __name__=='__main__':unittest.main()
