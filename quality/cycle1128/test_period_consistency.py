import importlib.util,json,pathlib,subprocess,tempfile,unittest
spec=importlib.util.spec_from_file_location('fix',pathlib.Path(__file__).with_name('period_consistency.py'))
fix=importlib.util.module_from_spec(spec);spec.loader.exec_module(fix)

def manifest(g='ai'):
 return {'policy':fix.POLICY,'asset_approval':'private_review_only','source_sha256':'a'*64,'genre':g,'period':{'month_labels':['4月','5月','6月'],'claimed_month_count':4,'corrected_month_count':3},'patch':{'start_frame':0,'end_frame':30,'digit_bbox':[301,694,334,737],'digit_origin':[306,691],'replacement':'3'}}
class Tests(unittest.TestCase):
 def test_ten_genres(self):
  for g in fix.GENRES:self.assertEqual(fix.validate(manifest(g),'a'*64,2),(0,30))
 def test_wrong_month_count(self):
  m=manifest();m['period']['corrected_month_count']=4
  with self.assertRaises(ValueError):fix.validate(m,'a'*64,2)
 def test_no_actual_error(self):
  m=manifest();m['period']['claimed_month_count']=3
  with self.assertRaises(ValueError):fix.validate(m,'a'*64,2)
 def test_reject_duplicate_month(self):
  m=manifest();m['period']['month_labels'][1]='4月'
  with self.assertRaises(ValueError):fix.validate(m,'a'*64,2)
 def test_reject_unapproved(self):
  m=manifest();m['asset_approval']='public'
  with self.assertRaises(ValueError):fix.validate(m,'a'*64,2)
 def test_reject_wrong_sha(self):
  with self.assertRaises(ValueError):fix.validate(manifest(),'b'*64,2)
 def test_reject_caption_overlap(self):
  m=manifest();m['patch']['digit_bbox']=[301,1700,334,1730]
  with self.assertRaises(ValueError):fix.validate(m,'a'*64,2)
 def test_reject_pii_and_unsafe_replacement(self):
  m=manifest();m['patch']['replacement']='09012345678'
  with self.assertRaises(ValueError):fix.validate(m,'a'*64,2)
 def test_overlay_pixel_changes(self):
  m=manifest();im=fix.overlay(1080,1920,m)
  self.assertEqual(im.getpixel((302,700))[3],255);self.assertIsNone(im.crop((0,1490,1080,1920)).getbbox())
 def test_synthetic_full_render(self):
  with tempfile.TemporaryDirectory() as td:
   d=pathlib.Path(td);s=d/'s.mp4';o=d/'o.mp4';j=d/'m.json';q=d/'q.json'
   subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=navy:s=540x960:r=30:d=2','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-shortest',str(s)],check=True)
   m=manifest();m['source_sha256']=fix.sha(s);j.write_text(json.dumps(m),encoding='utf8');r=fix.render(s,o,j,q)
   self.assertEqual(r['full_av_decode'],'PASS');self.assertEqual(r['frames'],60);self.assertEqual(r['subtitle_track_count'],0)
if __name__=='__main__':unittest.main()
