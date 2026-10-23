import importlib.util, tempfile, unittest
from pathlib import Path
import numpy as np
MODULE=Path(__file__).resolve().parents[1]/'src'/'audio_cue_renderer.py'
spec=importlib.util.spec_from_file_location('audio_cue_renderer',MODULE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class CaptionTests(unittest.TestCase):
 def test_10_genres(self):self.assertEqual(len(m.PALETTES),10)
 def test_16_phrases(self):self.assertEqual(len(m.WORDS),16)
 def test_429_frames(self):self.assertEqual(sum(m.FRAMES),429)
 def test_ass_time(self):self.assertEqual(m.clock(14.2),'0:00:14.20')
 def test_fails_closed_without_speech(self):
  with self.assertRaises(ValueError):m.align(np.zeros(720),.02)
 def test_8_scene_synthetic_voice(self):
  energy=np.zeros(720,dtype=np.float32)
  starts=np.cumsum([0]+list(m.FRAMES[:-1]))/30
  ends=np.cumsum(m.FRAMES)/30
  for ss,se in zip(starts,ends):
   energy[int((ss+.18)/.02):int((se-.18)/.02)]=.12
  cues=m.align(energy,.02)
  self.assertEqual(len(cues),16)
  self.assertAlmostEqual(cues[0][0],.16,delta=.04)
  self.assertTrue(all(en>st for st,en,_ in cues))
 def test_karaoke_and_utf8(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'cues.ass'
   m.write_ass(p,[(.2,1.,m.WORDS[0])],'science')
   txt=p.read_text(encoding='utf-8')
   self.assertIn('基板、',txt)
   self.assertIn(r'{\kf',txt)
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):m.write_ass('/tmp/should-not-write.ass',[],'wrong')
if __name__=='__main__':unittest.main()
