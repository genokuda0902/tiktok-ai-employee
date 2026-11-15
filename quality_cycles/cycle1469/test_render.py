import json,subprocess,unittest
from pathlib import Path
from render import SCENES
ROOT=Path(__file__).parent
class QA(unittest.TestCase):
 def test_caption_segments(self):
  self.assertEqual([(x[3],x[4]) for x in SCENES],[(0,2),(2,4),(4,6),(6,8)])
 def test_video_and_fail_closed_audio(self):
  p=ROOT/'cycle1469_REVIEW_ONLY.mp4';self.assertTrue(p.is_file())
  meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
  v=[s for s in meta['streams'] if s['codec_type']=='video'];a=[s for s in meta['streams'] if s['codec_type']=='audio']
  self.assertEqual((v[0]['width'],v[0]['height']),(720,1280));self.assertFalse(a,'No Japanese TTS: must not falsely claim narration')
  self.assertAlmostEqual(float(meta['format']['duration']),8,delta=.2)
 def test_caption_not_spoken(self):
  captions=json.loads((ROOT/'captions.json').read_text());self.assertEqual(len(captions),4)
  self.assertTrue(all(c['speech_verified'] is False for c in captions))
if __name__=='__main__':unittest.main()
