import unittest
from PIL import Image
from hook_before_after import GENRES, HOOK_FRAMES, SAFE_Y, render_frame, validate
class HookTests(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(GENRES),10)
 def test_allowed(self):validate('ai_work')
 def test_fail_closed(self):
  for g in GENRES[1:]:
   with self.assertRaises(ValueError):validate(g)
 def test_unknown(self):
  with self.assertRaises(ValueError):validate('unknown',True)
 def test_synthetic_other_genre(self):validate('science',True)
 def test_frame_dimensions(self):
  a=Image.new('RGB',(1080,1920),'red');b=Image.new('RGB',(1080,1920),'blue')
  self.assertEqual(render_frame(a,b,0).size,(1080,SAFE_Y))
 def test_hook_animated(self):
  a=Image.new('RGB',(1080,1920),'red');b=Image.new('RGB',(1080,1920),'blue')
  self.assertNotEqual(render_frame(a,b,0).tobytes(),render_frame(a,b,HOOK_FRAMES-1).tobytes())
 def test_frame_bounds(self):
  a=Image.new('RGB',(1080,1920),'red')
  with self.assertRaises(ValueError):render_frame(a,a,HOOK_FRAMES)
if __name__=='__main__':unittest.main()
