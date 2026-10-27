import hashlib, json, math, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import cinematic_motion_audit as m

class Cycle904Tests(unittest.TestCase):
 def sample(self):
  return {'genre':'ai_work','publication_approved':False,'employee_approval':False,
          'contains_private_data':False,'asset_rights_approved':False,
          'upload_media_to_github':False,'source_sha256':'a'*64}
 def test_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_scenes(self):
  self.assertEqual(sum(b-a+1 for a,b in m.SCENES),691)
  self.assertEqual(m.SCENES[0][0],0);self.assertEqual(m.SCENES[-1][1],690)
 def test_manifest(self):self.assertTrue(m.manifest_check(self.sample()))
 def test_all_genres(self):
  for g in m.GENRES:
   d=self.sample();d['genre']=g;self.assertTrue(m.manifest_check(d))
 def test_unknown_genre(self):
  d=self.sample();d['genre']='unknown'
  with self.assertRaises(ValueError):m.manifest_check(d)
 def test_missing_private_review(self):
  for k in ('publication_approved','employee_approval','contains_private_data','asset_rights_approved','upload_media_to_github'):
   d=self.sample();d.pop(k)
   with self.assertRaises(ValueError,msg=k):m.manifest_check(d)
 def test_any_approval_rejected(self):
  for k in ('publication_approved','employee_approval','contains_private_data','asset_rights_approved','upload_media_to_github'):
   d=self.sample();d[k]=True
   with self.assertRaises(ValueError,msg=k):m.manifest_check(d)
 def test_sha_fail(self):
  d=self.sample();d['source_sha256']='abc'
  with self.assertRaises(ValueError):m.manifest_check(d)
 def test_sha_file(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'x';p.write_bytes(b'abc')
   self.assertEqual(m.sha256(p),hashlib.sha256(b'abc').hexdigest())
 def test_zoom_safe(self):
  z=[m.zoom(i) for i in range(691)]
  self.assertGreaterEqual(min(z),1.002);self.assertLessEqual(max(z),1.023)
  self.assertGreater(max(z)-min(z),0.019)
 def test_subtitle_protection(self):
  self.assertIn('crop=1080:1300',m.filter_graph())
  self.assertIn('overlay=0:0',m.filter_graph())
  self.assertNotIn('1490',m.filter_graph())
 def test_release_gate(self):
  with self.assertRaises(PermissionError):m.release_gate({'employee_approval':True})
 def test_no_overwrite(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'same.mp4';p.write_bytes(b'123')
   with self.assertRaises(ValueError):m.render(p,p,'missing')
 def test_ffmpeg_synthetic_smoke(self):
  import shutil,subprocess
  if not shutil.which('ffmpeg'):self.skipTest('FFmpeg unavailable')
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'s.mp4'
   subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x142033:s=320x480:r=30:d=1',
                   '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1',
                   '-shortest','-c:v','libx264','-c:a','aac',str(p)],check=True)
   self.assertTrue(p.stat().st_size>1000)

if __name__=='__main__':unittest.main()
