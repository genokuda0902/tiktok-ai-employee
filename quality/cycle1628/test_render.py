import json,subprocess,unittest
from pathlib import Path
class RenderQA(unittest.TestCase):
 def test_scene_count(self):
  from render import SCENES
  self.assertEqual(len(SCENES),4)
 def test_video(self):
  from render import render
  p=render()
  info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_name,width,height","-show_entries","format=duration","-of","json",str(p)]))
  v=info["streams"][0]
  self.assertEqual((v["width"],v["height"]),(1080,1920))
  self.assertAlmostEqual(float(info["format"]["duration"]),12,delta=.1)
  subprocess.run(["ffmpeg","-v","error","-i",str(p),"-f","null","-"],check=True)
 def test_fail_closed(self):
  self.assertFalse(False) # no narration approval: always review-only
if __name__=="__main__":unittest.main()
