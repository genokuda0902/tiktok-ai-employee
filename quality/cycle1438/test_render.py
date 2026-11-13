import unittest,subprocess,json
from pathlib import Path
from render import SCENES
class TestRender(unittest.TestCase):
 def test_scenes(self): self.assertEqual(len(SCENES),3)
 def test_caption_text(self): self.assertTrue(all(a and b for a,b in SCENES))
 def test_video(self):
  p=Path(__file__).parent/"cycle1438_REVIEW_ONLY.mp4"
  d=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(p)]))
  v=next(x for x in d["streams"] if x["codec_type"]=="video")
  self.assertEqual((v["width"],v["height"]),(1080,1920))
  self.assertTrue(any(x["codec_type"]=="audio" for x in d["streams"]))
  self.assertAlmostEqual(float(d["format"]["duration"]),9,delta=.2)
if __name__=="__main__":unittest.main()
