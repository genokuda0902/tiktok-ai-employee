import json,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class RenderTest(unittest.TestCase):
 def test_source(self):
  s=(ROOT/'render.py').read_text()
  self.assertIn('SAFE REVIEW',s)
  self.assertIn('488*(f+1)/(fps*duration)',s)
 def test_render_and_probe(self):
  subprocess.run(['python','render.py'],cwd=ROOT,check=True)
  p=ROOT/'cycle1445_REVIEW_ONLY.mp4'
  data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
  v=next(x for x in data['streams'] if x['codec_type']=='video')
  self.assertEqual((v['width'],v['height'],v['r_frame_rate']),(1080,1920,'18/1'))
  self.assertFalse(any(x['codec_type']=='audio' for x in data['streams']))
  self.assertEqual((ROOT/'captions.srt').read_text().count('-->'),3)
  subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
if __name__=='__main__': unittest.main()
