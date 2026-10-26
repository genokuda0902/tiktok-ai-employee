import unittest, tempfile
from pathlib import Path
from PIL import Image
from verified_delta import GENRES, evidence, frame, safe_text, render, POLICY, START, COUNT, TOP, BOTTOM
from PIL import ImageDraw

class VerifiedDeltaTests(unittest.TestCase):
 def test_ten_genres_derive_before_after(self):
  for genre in GENRES:
   with self.subTest(genre=genre):
    e=evidence(genre)
    self.assertEqual(e['before']+1,e['after'])
    self.assertEqual(sum(e['source_a']),e['total_a'])
    self.assertEqual(sum(e['source_b']),e['total_b'])
 def test_ai_work_exact_source(self):
  e=evidence('ai_work')
  self.assertEqual((e['before'],e['after'],e['total_a'],e['total_b']),(17,18,46,29))
 def test_all_genres_render_key_frames(self):
  for genre in GENRES:
   for i in (0,27,50,87):
    with self.subTest(genre=genre,frame=i):
     self.assertEqual(frame(i,genre).size,(1080,BOTTOM-TOP))
 def test_safe_text_rejects_overflow(self):
  im=Image.new('RGB',(100,100));d=ImageDraw.Draw(im)
  with self.assertRaises(ValueError):safe_text(d,(0,0),'長すぎる日本語の文字列',10,36,'white')
 def test_unknown_genre_rejected(self):
  with self.assertRaises(ValueError):evidence('unknown')
 def test_frame_bounds(self):
  for i in (-1,COUNT):
   with self.assertRaises(ValueError):frame(i)
 def test_fail_closed_missing_input(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(FileNotFoundError):render(Path(t)/'missing.mp4',Path(t)/'out.mp4',POLICY)
 def test_never_approve_publication(self):
  self.assertFalse(POLICY['publication_approved'])
  self.assertFalse(POLICY['automatic_posting'])
  self.assertFalse(POLICY['external_upload'])
  self.assertFalse(POLICY['source_rights_reviewed'])
 def test_preserve_caption_roi_by_design(self):
  self.assertEqual((TOP,BOTTOM),(285,1450))
  self.assertLess(BOTTOM,1490)
  self.assertEqual(START,422)
 def test_immutable_source_evidence(self):
  self.assertEqual(GENRES['ai_work'].a,(12,16,18))
  self.assertEqual(GENRES['ai_work'].b,(8,9,12))

if __name__=='__main__':unittest.main()