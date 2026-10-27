import unittest
from pathlib import Path
import tempfile
import sys
sys.path.insert(0,str(Path(__file__).parent))
import evidence_wipe as e

class EvidenceWipeTests(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(e.PALETTES),10)
  self.assertEqual(set(e.PALETTES),set(e.GENRE_LABELS))
 def test_review_only(self):self.assertIn('PUBLICATION_NOT_APPROVED',e.POLICY)
 def test_safe_area(self):self.assertLess(e.OVERLAY_Y+e.H,e.SUBTITLE_Y)
 def test_scene_duration(self):self.assertEqual(e.END_FRAME-e.START_FRAME,103)
 def test_scene_bounds(self):self.assertEqual(e.END_FRAME,691)
 def test_no_external_assets(self):
  text=Path(e.__file__).read_text()
  self.assertNotIn('requests.get',text)
  self.assertNotIn('http://',text)
 def test_reject_bad_genre(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   with self.assertRaises(ValueError):e.render(p/'none.mp4',p/'test_REVIEW_ONLY.mp4','0'*64,'not_a_genre',p/'frames')
 def test_reject_public_filename(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   with self.assertRaises(ValueError):e.render(p/'none.mp4',p/'publish.mp4','0'*64,'ai_work',p/'frames')
 def test_reject_wrong_sha(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'source.mp4').write_bytes(b'private')
   with self.assertRaises(ValueError):e.render(p/'source.mp4',p/'test_REVIEW_ONLY.mp4','0'*64,'ai_work',p/'frames')
 def test_never_overwrite(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);f=p/'same_REVIEW_ONLY.mp4';f.write_bytes(b'a')
   with self.assertRaises(ValueError):e.render(f,f,'0'*64,'ai_work',p/'frames')
 def test_caption_is_outside_overlay(self):self.assertGreater(e.SUBTITLE_Y,e.OVERLAY_Y+e.H)
 def test_palette_colors(self):
  for a,b in e.PALETTES.values():
   self.assertRegex(a,r'^#[0-9a-f]{6}$');self.assertRegex(b,r'^#[0-9a-f]{6}$')
if __name__=='__main__':unittest.main()
