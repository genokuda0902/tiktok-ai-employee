import importlib.util, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('kinetic_hook',Path(__file__).with_name('kinetic_hook.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestHook(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_policy(self):self.assertEqual(m.POLICY,'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED')
 def test_safe_region(self):self.assertLess(m.TOP+m.ART_H,m.CAPTION_START)
 def test_frame_count(self):self.assertEqual(m.FRAMES,87)
 def test_phases(self):self.assertEqual([m.phase(x) for x in (0,31,32,60,61,86)],[0,0,1,1,2,2])
 def test_phase_bounds(self):
  for x in (-1,87):
   with self.assertRaises(ValueError):m.phase(x)
 def test_smooth(self):self.assertEqual((m.smooth(-1),m.smooth(2)),(0,1))
 def test_safe_text(self):self.assertIn('架空',m.GENRES['ai_work'][1])
 def test_unknown_genre(self):
  with tempfile.TemporaryDirectory() as td:
   src=Path(td)/'src.mp4';src.write_bytes(b'private')
   with self.assertRaisesRegex(ValueError,'genre'):m.validate(src,Path(td)/'out_REVIEW_ONLY.mp4',m.sha256(src),'invalid')
 def test_sha(self):
  with tempfile.TemporaryDirectory() as td:
   src=Path(td)/'src.mp4';src.write_bytes(b'private')
   with self.assertRaisesRegex(ValueError,'SHA'):m.validate(src,Path(td)/'out_REVIEW_ONLY.mp4','bad','ai_work')
 def test_review_only(self):
  with tempfile.TemporaryDirectory() as td:
   src=Path(td)/'src.mp4';src.write_bytes(b'private')
   with self.assertRaisesRegex(ValueError,'review-only output'):m.validate(src,Path(td)/'out.mp4',m.sha256(src),'ai_work')
 def test_policy_gate(self):
  with tempfile.TemporaryDirectory() as td:
   src=Path(td)/'src.mp4';src.write_bytes(b'private')
   with self.assertRaisesRegex(ValueError,'policy'):m.validate(src,Path(td)/'out_REVIEW_ONLY.mp4',m.sha256(src),'ai_work','APPROVED')
 def test_overwrite(self):
  with tempfile.TemporaryDirectory() as td:
   src=Path(td)/'src_REVIEW_ONLY.mp4';src.write_bytes(b'private')
   with self.assertRaisesRegex(ValueError,'overwrite'):m.validate(src,src,m.sha256(src),'ai_work')
 @unittest.skipUnless(importlib.util.find_spec("PIL") and Path(m.FONT).is_file(), "optional Pillow/Noto font absent")
 def test_render_one_frame(self):
  from PIL import ImageFont
  fonts=(ImageFont.truetype(m.FONT,75),ImageFont.truetype(m.FONT,72),ImageFont.truetype(m.FONT,38),ImageFont.truetype(m.REG,31))
  img=m.draw_frame(62,'ai_work',m.make_background(),fonts)
  self.assertEqual(img.size,(m.W,m.ART_H))
if __name__=='__main__':unittest.main()
