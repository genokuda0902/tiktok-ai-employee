import importlib.util,tempfile,subprocess,unittest
from pathlib import Path
from PIL import Image
P=Path(__file__).parent/'chapter_number_fix.py';spec=importlib.util.spec_from_file_location('chapter',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ChapterFixTests(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(m.PALETTES),10)
 def test_patch_only_header(self):
  with tempfile.TemporaryDirectory() as d:
   for genre in m.PALETTES:
    p=Path(d)/(genre+'.png');m.make_patch(p,genre)
    im=Image.open(p)
    self.assertEqual(im.getpixel((100,100))[3],0)
    self.assertEqual(im.getpixel((100,1280))[3],0)
    self.assertGreater(im.getpixel((190,110))[3],0)
 def test_refuse_other_scene(self):
  with self.assertRaises(ValueError):m.make_patch('/tmp/x.png','ai',3,8)
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):m.make_patch('/tmp/x.png','other')
 def test_integrated_synthetic_mp4(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'in.mp4';out=Path(d)/'out.mp4'
   subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x031021:s=1080x1920:r=30:d=1',
                   '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1',
                   '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)],check=True)
   sha=m.sha(src)
   with self.assertRaisesRegex(ValueError,'SHA'):m.validate(src,out,'0'*64,'ai',2,8,(.1,.8))
   with self.assertRaisesRegex(ValueError,'overwrite'):m.validate(src,src,sha,'ai',2,8,(.1,.8))
   with self.assertRaisesRegex(ValueError,'observed'):m.validate(src,out,sha,'ai',3,8,(.1,.8))
   r=m.render(src,out,sha,times=(.1,.8));self.assertEqual(r['frames'],30)
   self.assertTrue(r['audio_bitstream_identical'])
   subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
if __name__=='__main__':unittest.main()
