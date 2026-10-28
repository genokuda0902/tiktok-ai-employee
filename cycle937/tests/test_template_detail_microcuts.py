import unittest,sys
from pathlib import Path
from PIL import Image,ImageChops
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from template_detail_microcuts import *

class MicrocutTests(unittest.TestCase):
 def setUp(self):
  self.frame=Image.new('RGB',(1080,1920),(38,65,87))
 def test_ten_genres(self):self.assertEqual(len(GENRES),10)
 def test_ten_genre_render(self):
  for genre in GENRES:
   with self.subTest(genre=genre):self.assertEqual(make_overlay(28,self.frame,genre).size,(1080,1450))
 def test_two_shots(self):self.assertEqual([beat(i) for i in (0,18,19,37,38,59)],[0,0,1,1,2,2])
 def test_bad_frames(self):
  for f in (-1,60):
   with self.assertRaises(ValueError):beat(f)
 def test_reject_bad_genre(self):
  with self.assertRaises(ValueError):validate('wrong')
 def test_reject_bad_source_size(self):
  with self.assertRaises(ValueError):validate('ai_work',Image.new('RGB',(600,1000)))
 def test_real_difference(self):
  a=make_overlay(8,self.frame);b=make_overlay(28,self.frame)
  self.assertIsNotNone(ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox())
 def test_exact_frame_geometry(self):self.assertEqual((SCENE_END-SCENE_START,OVERLAY_END-OVERLAY_START),(87,60))
 def test_subtitle_safe(self):self.assertLessEqual(SAFE_Y,1450)
 def test_publication_guard(self):self.assertIn('PUBLICATION_NOT_APPROVED',POLICY)
 def test_fails_closed_on_unknown_source(self):
  from tempfile import TemporaryDirectory
  with TemporaryDirectory() as d:
   source=Path(d)/'input.mp4';source.write_bytes(b'fake')
   with self.assertRaisesRegex(RuntimeError,'SOURCE_SHA'):render(source,Path(d)/'out.mp4',Path(d)/'tmp')
 def test_no_external_media_requests(self):
  import inspect
  code=inspect.getsource(render)
  self.assertNotIn('requests.',code)
  self.assertNotIn('upload(',code)
 def test_outro_requires_explicit_frame(self):
  with self.assertRaises(ValueError):make_overlay(45,self.frame)
 def test_outro_preserves_source_image(self):
  outro=Image.new('RGB',(1080,1920),(20,30,40))
  self.assertEqual(make_overlay(45,self.frame,outro_frame=outro).getpixel((1,1)),(20,30,40,255))
 def test_frame_content_does_not_include_caption_band(self):
  self.assertEqual(make_overlay(1,self.frame).height,1450)

if __name__=='__main__':unittest.main()
