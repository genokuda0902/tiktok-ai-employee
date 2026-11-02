import importlib.util
import unittest
from pathlib import Path
import tempfile
import json
import subprocess

spec=importlib.util.spec_from_file_location('proof_share_bars',Path(__file__).with_name('proof_share_bars.py'))
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)


def manifest(genre='ai'):
 return {'policy':p.POLICY,'asset_approval':'private_review_only','source_sha256':'abc',
         'genre':genre,'scene_start':0.3,'scene_end':2.4,
         'values':[46,29,75],'monthly_rows':[[12,8],[16,9],[18,12]],
         'roi':{'x':60,'y':895,'width':960,'height':50}}

class ProofShareBarsTest(unittest.TestCase):
 def setUp(self):
  self.s={'width':1080,'height':1920,'duration':3.0}
 def test_all_ten_genres(self):
  for g in p.GENRES:
   with self.subTest(genre=g):self.assertEqual(p.validate_manifest(manifest(g),'abc',self.s),(.3,2.4))
 def test_sum_mismatch_rejected(self):
  m=manifest();m['values']=[46,29,74]
  with self.assertRaisesRegex(ValueError,'total'):p.validate_manifest(m,'abc',self.s)
 def test_row_mismatch_rejected(self):
  m=manifest();m['monthly_rows'][1][0]=17
  with self.assertRaisesRegex(ValueError,'row'):p.validate_manifest(m,'abc',self.s)
 def test_private_approval_and_hash(self):
  for key,value in [('asset_approval','public'),('policy','PUBLISH'),('source_sha256','wrong')]:
   m=manifest();m[key]=value
   with self.assertRaises(ValueError):p.validate_manifest(m,'abc',self.s)
 def test_subtitle_safe_region(self):
  m=manifest();m['roi']['y']=1320
  with self.assertRaisesRegex(ValueError,'ROI'):p.validate_manifest(m,'abc',self.s)
 def test_unknown_genre(self):
  m=manifest('other')
  with self.assertRaisesRegex(ValueError,'genre'):p.validate_manifest(m,'abc',self.s)
 def test_frame_boundaries(self):
  m=manifest();m['scene_start']=0.31
  with self.assertRaisesRegex(ValueError,'frame'):p.validate_manifest(m,'abc',self.s)
 def test_eased_progress_and_bar_ratio(self):
  self.assertEqual(p.eased(-1),0);self.assertEqual(p.eased(3),1)
  a=p.draw_overlay_frame(manifest(),2.2)
  self.assertEqual(a.size,(960,50))
  # filled bar pixels, 46/75 and 29/75, total exactly 75/75
  self.assertGreater(a.getpixel((45,24))[3],0)
  self.assertGreater(a.getpixel((385,24))[3],0)
  self.assertGreater(a.getpixel((900,24))[3],0)
 def test_synthetic_video_end_to_end(self):
  with tempfile.TemporaryDirectory() as td:
   td=Path(td);src=td/'input.mp4';out=td/'output.mp4';qa=td/'qa.json'
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=navy:s=1080x1920:r=30:d=3',
                   '-f','lavfi','-i','sine=frequency=220:sample_rate=48000:duration=3',
                   '-c:v','libx264','-preset','ultrafast','-crf','36','-pix_fmt','yuv420p','-c:a','aac','-b:a','64k',
                   '-metadata:s:a:0','language=jpn',str(src)],check=True)
   m=manifest();m['source_sha256']=p.sha256(src)
   res=p.render(src,out,m,qa)
   self.assertEqual(res['frames'],90)
   self.assertEqual(res['rendered_overlay_frames'],63)
   self.assertEqual(res['subtitle_streams'],0)
   self.assertTrue(out.exists())
   self.assertEqual(json.loads(qa.read_text())['values'],[46,29,75])

if __name__=='__main__':unittest.main()
