import copy,json,unittest,tempfile
from pathlib import Path
from caption_timeline import validate,build_ass,GENRES,ass_time
M=json.loads((Path(__file__).parent/'captions.json').read_text(encoding='utf-8'))
class CaptionTest(unittest.TestCase):
 def test_manifest(self): self.assertEqual(len(validate(M)),8)
 def test_all_ten_genres(self):
  for g in GENRES:
   d=copy.deepcopy(M);d['genre']=g;self.assertEqual(len(validate(d)),8)
 def test_disallow_posting(self):
  for key,value in [('publication','APPROVED'),('auto_post',True),('human_review','APPROVED')]:
   d=copy.deepcopy(M);d[key]=value
   with self.assertRaises(ValueError):validate(d)
 def test_rights(self):
  d=copy.deepcopy(M);d['rights']='unknown'
  with self.assertRaises(ValueError):validate(d)
 def test_voice_gate(self):
  d=copy.deepcopy(M);d['narration_status']='VERIFIED'
  with self.assertRaises(ValueError):validate(d)
 def test_timing(self):
  for start,end in [(2,2),(19,21),(-1,2),(1,1.5)]:
   d=copy.deepcopy(M);d['captions'][0].update(start=start,end=end)
   with self.assertRaises(ValueError):validate(d)
 def test_gaps_or_overlap_rejected(self):
  for start in (2.4,2.6):
   d=copy.deepcopy(M);d['captions'][1]['start']=start
   with self.assertRaises(ValueError):validate(d)
 def test_ass_file(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'caption.ass';build_ass(M,p);s=p.read_text(encoding='utf-8')
   self.assertEqual(s.count('Dialogue:'),8);self.assertIn('SUM関数で合計を計算',s)
   self.assertIn('MarginV',s)
 def test_ass_time(self): self.assertEqual(ass_time(12.5),'0:00:12.50')
 def test_injection_rejected(self):
  d=copy.deepcopy(M);d['captions'][0]['text']='{\\pos(0,0)}'
  with self.assertRaises(ValueError):validate(d)
if __name__=='__main__':unittest.main()
