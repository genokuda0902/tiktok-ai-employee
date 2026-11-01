import json
import tempfile
import unittest
from pathlib import Path
from scene_focus import (GENRES,POLICY,APPROVAL,safe_label,validate_manifest,make_overlay,export,digest,execute,probe)

class FocusTests(unittest.TestCase):
    def template(self,genre='ai'):
        return {'policy':POLICY,'asset_approval':APPROVAL,'source_sha256':'abc','genre':genre,
                'focus_scene':{'start':0.2,'split':0.7,'end':1.2,'focuses':[
                    {'label':'01 FORMULA','rect':[40,60,90,30],'badge_xy':[30,100]},
                    {'label':'02 RESULT','rect':[50,120,110,50],'badge_xy':[30,100]}]}}
    def test_genres(self):
        for genre in GENRES:
            with self.subTest(genre=genre):validate_manifest(self.template(genre),'abc',540,960,2)
    def test_wrong_hash(self):
        with self.assertRaises(ValueError):validate_manifest(self.template(),'other',540,960,2)
    def test_reject_unknown_genre(self):
        m=self.template();m['genre']='unlisted'
        with self.assertRaises(ValueError):validate_manifest(m,'abc',540,960,2)
    def test_reject_bad_timing(self):
        m=self.template();m['focus_scene']['split']=0.1
        with self.assertRaises(ValueError):validate_manifest(m,'abc',540,960,2)
    def test_reject_caption_overlap(self):
        m=self.template();m['focus_scene']['focuses'][0]['rect']=[30,700,100,50]
        with self.assertRaises(ValueError):validate_manifest(m,'abc',540,960,2)
    def test_reject_pii(self):
        with self.assertRaises(ValueError):safe_label('abc@example.com')
    def test_render_overlay(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'overlay.png'
            make_overlay(self.template()['focus_scene']['focuses'][0],540,960,p,(0,255,200))
            self.assertGreater(p.stat().st_size,1000)
    def test_synthetic_video_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);src=p/'input.mp4';out=p/'out.mp4';mf=p/'manifest.json';qa=p/'qa.json'
            execute(['ffmpeg','-v','error','-f','lavfi','-i','color=c=navy:s=540x960:r=30:d=2',
                     '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
                     '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)])
            m=self.template();m['source_sha256']=digest(src);mf.write_text(json.dumps(m))
            result=export(src,out,mf,qa)
            self.assertEqual(result['frames'],60)
            self.assertEqual(result['full_decode'],'PASS')
            self.assertTrue(result['audio_elementary_unchanged'])
            self.assertEqual(len([s for s in probe(out)['streams'] if s['codec_type']=='subtitle']),0)
            with self.assertRaises(FileExistsError):export(src,out,mf,qa)

if __name__=='__main__':unittest.main()
