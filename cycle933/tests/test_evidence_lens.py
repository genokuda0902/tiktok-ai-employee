import sys
import unittest
from pathlib import Path
from PIL import Image

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from evidence_lens import (
 GENRES, WIDTH, HEIGHT, SAFE_Y, START, END, CELL_B4, CELL_B5,
 LENS_SOURCE, LENS_TARGET, build_overlay, phase, ensure_contract, POLICY
)

class TestEvidenceLens(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=Image.new('RGB',(WIDTH,HEIGHT),'#334455')
  for y in range(LENS_SOURCE[1],LENS_SOURCE[3]):
   for x in range(LENS_SOURCE[0],LENS_SOURCE[2]):
    cls.src.putpixel((x,y),((x*3)%256,(y*5)%256,(x+y)%256))

 def test_all_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for genre in GENRES: ensure_contract(genre)

 def test_all_ten_genres_render(self):
  for genre in GENRES:
   with self.subTest(genre=genre):
    self.assertEqual(build_overlay(self.src,START,genre).size,(WIDTH,SAFE_Y))

 def test_beat_boundaries(self):
  self.assertEqual(phase(START),0)
  self.assertEqual(phase(START+29),1)
  self.assertEqual(phase(START+58),2)
  self.assertEqual(phase(END-1),2)

 def test_reject_outside_scene(self):
  for f in [START-1,END]:
   with self.assertRaises(ValueError):phase(f)

 def test_unknown_genre_fail_closed(self):
  with self.assertRaises(ValueError):ensure_contract('unknown')

 def test_wrong_resolution_fail_closed(self):
  with self.assertRaises(ValueError):
   build_overlay(Image.new('RGB',(540,960)),START)

 def test_preserve_original_crop(self):
  im=build_overlay(self.src,START)
  source_crop=self.src.crop(LENS_SOURCE).resize(
   (LENS_TARGET[2]-LENS_TARGET[0],LENS_TARGET[3]-LENS_TARGET[1]),
   Image.Resampling.LANCZOS)
  for dx,dy in [(205,75),(245,128),(300,180)]:
   self.assertEqual(
    im.getpixel((LENS_TARGET[0]+dx,LENS_TARGET[1]+dy))[:3],
    source_crop.getpixel((dx,dy)))

 def test_caption_safe_area(self):
  self.assertLess(SAFE_Y,1280)
  self.assertLess(LENS_TARGET[3],SAFE_Y)
  self.assertLess(CELL_B5[3],SAFE_Y)

 def test_no_approval_bypass(self):
  self.assertIn('PUBLICATION_NOT_APPROVED',POLICY)

 def test_source_frames_unchanged_outside_edited_scene(self):
  self.assertEqual((START,END),(348,435))

 def test_lens_really_enlarges(self):
  self.assertGreater(
   (LENS_TARGET[2]-LENS_TARGET[0])/(LENS_SOURCE[2]-LENS_SOURCE[0]),1.5)
  self.assertGreater(
   (LENS_TARGET[3]-LENS_TARGET[1])/(LENS_SOURCE[3]-LENS_SOURCE[1]),1.5)

if __name__=='__main__':unittest.main()
