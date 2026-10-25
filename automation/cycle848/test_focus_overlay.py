import json
import unittest
from pathlib import Path
from focus_overlay import GENRES,POLICY,SIZE,TARGETS,make_filter,validate

BEATS=json.loads((Path(__file__).parent/'caption_beats.json').read_text(encoding='utf-8'))
class TestFocus(unittest.TestCase):
 def test_24_beats(self):self.assertTrue(validate(BEATS,'ai_work',POLICY))
 def test_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for g in GENRES:self.assertTrue(validate(BEATS,g,POLICY))
 def test_24_independent_focuses(self):
  self.assertEqual(sum(len(x) for x in TARGETS),24)
  self.assertEqual(make_filter(BEATS).count('t=5:enable='),24)
 def test_subtitle_safe_zone(self):
  self.assertTrue(all(y+h<1390 for scene in TARGETS for x,y,w,h in scene))
 def test_video_size(self):self.assertEqual(SIZE,(1080,1920))
 def test_reject_publish(self):
  with self.assertRaises(ValueError):validate(BEATS,'ai_work',{**POLICY,'publication_approved':True})
 def test_reject_upload(self):
  with self.assertRaises(ValueError):validate(BEATS,'ai_work',{**POLICY,'external_upload':True})
 def test_reject_post(self):
  with self.assertRaises(ValueError):validate(BEATS,'ai_work',{**POLICY,'automatic_posting':True})
 def test_reject_unsupported(self):
  with self.assertRaises(ValueError):validate(BEATS,'unsupported',POLICY)
 def test_reject_bad_timing(self):
  wrong=[dict(b) for b in BEATS];wrong[2]['start']=0.3
  with self.assertRaises(ValueError):validate(wrong,'ai_work',POLICY)
 def test_filter_contains_timed_enable(self):
  f=make_filter(BEATS)
  self.assertIn('between(t,0.270,0.930)',f)
  self.assertIn('between(t,22.030,23.030)',f)
 def test_no_network(self):
  import inspect,focus_overlay
  source=inspect.getsource(focus_overlay)
  self.assertNotIn('requests.',source)
  self.assertNotIn('http://',source)
  self.assertNotIn('https://',source)
if __name__=='__main__':unittest.main()
