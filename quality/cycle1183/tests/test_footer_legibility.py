import importlib.util
import pathlib
import subprocess
import tempfile
import unittest

P=pathlib.Path(__file__).resolve().parents[1]/'code'/'footer_legibility.py'
spec=importlib.util.spec_from_file_location('footer_legibility',P)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class FooterLegibilityTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(mod.GENRE_ACCENTS),10)
    def test_genre_accents_are_hex(self):
        self.assertTrue(all(c.startswith('0x') and len(c)==8 for c in mod.GENRE_ACCENTS.values()))
    def test_reject_unknown_genre(self):
        with self.assertRaisesRegex(ValueError,'genre'):
            mod.validate({'streams':[]},'unknown')
    def test_reject_subtitle_overlap(self):
        with self.assertRaisesRegex(ValueError,'footer'):
            mod.validate({'streams':[]},'ai',(68,1450,944,128))
    def test_reject_out_of_frame(self):
        with self.assertRaisesRegex(ValueError,'footer'):
            mod.validate({'streams':[]},'ai',(68,1840,944,128))
    def test_graph_has_two_japanese_lines(self):
        g=mod.graph('ai','/tmp/font.ttc','/tmp/line1','/tmp/line2')
        self.assertEqual(g.count('drawtext='),2)
        self.assertIn('y=1740',g)
        self.assertIn('fontsize=28',g)
    def test_no_source_overwrite(self):
        with self.assertRaisesRegex(ValueError,'overwrite'):
            mod.render('/tmp/same.mp4','/tmp/same.mp4')
    def test_bad_topic_rejected(self):
        with self.assertRaises(ValueError):mod.render('/tmp/in.mp4','/tmp/out.mp4',topic='line1\nline2')
    def test_synthetic_render_and_decode(self):
        with tempfile.TemporaryDirectory() as d:
            src=pathlib.Path(d)/'src.mp4';out=pathlib.Path(d)/'out.mp4'
            subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y',
                '-f','lavfi','-i','color=c=0x06121e:s=1080x1920:r=30:d=1',
                '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1',
                '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
                '-c:a','aac','-shortest',str(src)],check=True)
            r=mod.render(src,out)
            self.assertEqual(r['frames'],30)
            subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
            self.assertEqual(int(next(s for s in mod.probe(out)['streams']
                                if s['codec_type']=='video')['nb_frames']),30)

if __name__=='__main__': unittest.main()
