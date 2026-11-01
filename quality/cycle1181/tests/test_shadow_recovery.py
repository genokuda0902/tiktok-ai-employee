import importlib.util
import pathlib
import subprocess
import tempfile
import unittest

P=pathlib.Path(__file__).resolve().parents[1]/'code'/'shadow_recovery.py'
spec=importlib.util.spec_from_file_location('shadow_recovery',P)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ShadowRecoveryTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(mod.GENRE_GAMMA),10)
    def test_gamma_is_bounded(self):
        self.assertTrue(all(1.0 < g <= 1.16 for g in mod.GENRE_GAMMA.values()))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):mod.validate({'streams':[]},'unknown',mod.DEFAULT_ROI)
    def test_roi_protects_subtitles(self):
        with self.assertRaisesRegex(ValueError,'protected'):mod.validate({'streams':[]},'ai',(60,1200,960,300))
    def test_roi_protects_header(self):
        with self.assertRaisesRegex(ValueError,'protected'):mod.validate({'streams':[]},'ai',(60,200,960,300))
    def test_roi_rejects_odd_chroma(self):
        with self.assertRaises(ValueError):mod.validate({'streams':[]},'ai',(61,390,960,930))
    def test_graph_is_panel_only(self):
        self.assertIn('crop=960:930:60:390',mod.graph('ai',mod.DEFAULT_ROI))
        self.assertIn('overlay=60:390',mod.graph('ai',mod.DEFAULT_ROI))
    def test_no_overwrite(self):
        with self.assertRaises(ValueError):mod.render('/tmp/same.mp4','/tmp/same.mp4')
    def test_synthetic_mp4(self):
        with tempfile.TemporaryDirectory() as d:
            source=pathlib.Path(d)/'in.mp4';out=pathlib.Path(d)/'out.mp4'
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
              '-f','lavfi','-i','color=c=0x07202a:s=1080x1920:r=30:d=1',
              '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1',
              '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
              '-c:a','aac','-shortest',str(source)],check=True)
            result=mod.render(source,out)
            self.assertEqual(result['frames'],30)
            subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),
                            '-f','null','-'],check=True)
            self.assertEqual(int(next(s for s in mod.probe(out)['streams']
                                  if s['codec_type']=='video')['nb_frames']),30)

if __name__=='__main__':unittest.main()
