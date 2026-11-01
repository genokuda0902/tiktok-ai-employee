import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from PIL import Image
P=Path(__file__).parent/'safety_disclaimer.py'
spec=importlib.util.spec_from_file_location('disclaimer',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class DisclaimerTests(unittest.TestCase):
    def test_ten_genres_and_wcag_aaa(self):
        self.assertEqual(len(m.GENRE_ACCENTS),10)
        for g in m.GENRE_ACCENTS: self.assertEqual(m.validate_config(g),g)
    def test_unknown_genre_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'unknown genre'):m.validate_config('unknown')
    def test_contrast_threshold(self):
        self.assertGreaterEqual(m.contrast(m.WHITE,m.BG),7)
        for v in m.GENRE_ACCENTS.values():self.assertGreaterEqual(m.contrast(v,m.BG),7)
    def test_caption_safe_all_palettes(self):
        with tempfile.TemporaryDirectory() as d:
            for g in m.GENRE_ACCENTS:
                f=Path(d)/(g+'.png');m.make_overlay(f,g)
                im=Image.open(f)
                self.assertEqual(im.size,(1080,1920))
                self.assertEqual(im.getpixel((150,1350))[3],0)
                self.assertEqual(im.getpixel((500,900))[3],0)
                self.assertGreater(im.getpixel((75,1110))[3],0)
    def test_timing_gate(self):
        with self.assertRaises(ValueError):m.validate_config('unsafe')
    def test_synthetic_h264_aac_smoke(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/'src.mp4';dst=Path(d)/'dst.mp4'
            subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x091828:s=1080x1920:r=30:d=18',
                            '-f','lavfi','-i','sine=frequency=500:sample_rate=48000:duration=18',
                            '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)],check=True)
            s=m.sha(src)
            with self.assertRaisesRegex(ValueError,'SHA'):m.validate_source(src,dst,'0'*64,'ai')
            with self.assertRaisesRegex(ValueError,'overwrite'):m.validate_source(src,src,s,'ai')
            with self.assertRaisesRegex(ValueError,'scene06'):m.validate_source(src,dst,s,'ai',(1,2))
            result=m.render(src,dst,s)
            self.assertEqual(result['frames'],540)
            self.assertTrue(result['audio_adts_identical'])
            subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(dst),'-f','null','-'],check=True)

if __name__=='__main__':unittest.main()
