"""cycle806 contract tests: no assets, network or paid dependencies."""
import importlib.util,json,unittest
from pathlib import Path
from PIL import ImageChops
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('overlay806',ROOT/'overlay806.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class KineticCaptionTests(unittest.TestCase):
 def setUp(self):self.voice=json.loads((ROOT/'voice_timing.json').read_text(encoding='utf-8'))
 def test_ten_genres(self):self.assertEqual(len(m.GENRES),len(m.COLORS))
 def test_8_scene_timing(self):
  n=m.counts(self.voice);self.assertEqual(len(n),8);self.assertEqual(sum(n),775)
 def test_keywords_are_in_narration(self):
  for k,s in zip(m.KEYS,self.voice['sentences']):self.assertIn(k,s['text'])
 def test_caption_safe_two_lines(self):
  for s in self.voice['sentences']:
   for size in (54,51,48,45,42):
    lines=m.lines(s['text'],m.font(size))
    if len(lines)<=2:break
   self.assertLessEqual(len(lines),2)
 def test_emphasis_actually_changes_pixels(self):
  a=m.overlay(self.voice['sentences'][0]['text'],m.KEYS[0],0,0,m.COLORS[4])
  b=m.overlay(self.voice['sentences'][0]['text'],m.KEYS[0],0,1,m.COLORS[4])
  self.assertIsNotNone(ImageChops.difference(a,b).getbbox())
 def test_invalid_duration_rejected(self):
  v=json.loads(json.dumps(self.voice));v['sentences'][0]['seconds']=-1
  with self.assertRaises(ValueError):m.counts(v)
 def test_unknown_genre_rejected(self):
  with self.assertRaises(ValueError):m.render('not-found.mp4',ROOT/'voice_timing.json','out.mp4','not-a-genre')
 def test_review_only(self):self.assertEqual(self.voice['status'],'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED')
if __name__=='__main__':unittest.main()
