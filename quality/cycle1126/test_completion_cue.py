import hashlib, importlib.util, json, pathlib, subprocess, sys, tempfile, unittest
P=pathlib.Path(__file__).with_name('completion_cue.py')
spec=importlib.util.spec_from_file_location('cue',P);cue=importlib.util.module_from_spec(spec);spec.loader.exec_module(cue)

def manifest(genre='ai'):
    return {'policy':cue.POLICY,'asset_approval':cue.APPROVAL,'source_sha256':'a'*64,'genre':genre,'cue':{'start':0.0,'switch':0.5,'end':1.0,'steps':[{'rect':[.1,.2,.35,.1],'label':'02 保存する'},{'rect':[.55,.2,.35,.1],'label':'03 次回も再利用'}]}}
class CueTests(unittest.TestCase):
    def test_all_genres(self):
        for g in cue.GENRES:
            with self.subTest(genre=g):self.assertEqual(cue.validate(manifest(g),'a'*64,540,960,1.5),(0,.5,1.))
    def test_source_hash(self):
        with self.assertRaises(ValueError):cue.validate(manifest(),'b'*64,540,960,1.5)
    def test_reject_unapproved(self):
        m=manifest();m['asset_approval']='public';
        with self.assertRaises(ValueError):cue.validate(m,'a'*64,540,960,1.5)
    def test_reject_pii(self):
        m=manifest();m['cue']['steps'][1]['label']='09012345678';
        with self.assertRaises(ValueError):cue.validate(m,'a'*64,540,960,1.5)
    def test_reject_subtitle_overlap(self):
        m=manifest();m['cue']['steps'][1]['rect']=[.5,.85,.35,.1];
        with self.assertRaises(ValueError):cue.validate(m,'a'*64,540,960,1.5)
    def test_reject_off_grid(self):
        m=manifest();m['cue']['switch']=.51;
        with self.assertRaises(ValueError):cue.validate(m,'a'*64,540,960,1.5)
    def test_animation_changes(self):
        a=cue.overlay_frame(540,960,manifest()['cue']['steps'],.3,0,.5,1)
        b=cue.overlay_frame(540,960,manifest()['cue']['steps'],.8,0,.5,1)
        self.assertNotEqual(a.tobytes(),b.tobytes());self.assertEqual(a.getbbox() is not None,True)
    def test_synthetic_render(self):
        with tempfile.TemporaryDirectory() as t:
            t=pathlib.Path(t);src=t/'s.mp4';out=t/'o.mp4';m=t/'m.json';qa=t/'qa.json'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=navy:s=540x960:r=30:d=1.5','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1.5','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-shortest',str(src)],check=True)
            conf=manifest();conf['source_sha256']=cue.sha(src);m.write_text(json.dumps(conf),encoding='utf8')
            report=cue.export(src,out,m,qa)
            self.assertEqual(report['full_decode'],'PASS');self.assertEqual(report['soft_subtitles'],0)
            self.assertTrue(out.stat().st_size>1000)
            with self.assertRaises(FileExistsError):cue.export(src,out,m,qa)
if __name__=='__main__':unittest.main()
