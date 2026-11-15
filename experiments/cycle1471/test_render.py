import json, subprocess, pathlib, unittest
from render import render,SCENES
class ReviewTest(unittest.TestCase):
 def test_scene_count(self):self.assertEqual(len(SCENES),4)
 def test_render_and_probe(self):
  out=render(pathlib.Path(__file__).parent/'cycle1471_REVIEW_ONLY.mp4')
  data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height:format=duration','-of','json',str(out)]))
  self.assertAlmostEqual(float(data['format']['duration']),12,delta=.15)
  v=[s for s in data['streams'] if s['codec_type']=='video'][0]
  self.assertEqual((v['width'],v['height']),(720,1280))
  self.assertEqual(v['codec_name'],'h264')
  self.assertFalse(any(s['codec_type']=='audio' for s in data['streams']))
  subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
  self.assertEqual((out.parent/'captions.srt').read_text().count(' --> '),4)
if __name__=='__main__':unittest.main()
