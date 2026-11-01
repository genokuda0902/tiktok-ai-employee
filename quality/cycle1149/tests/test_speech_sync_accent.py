import importlib.util, unittest, numpy as np
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'code'/'speech_sync_accent.py'
s=importlib.util.spec_from_file_location('accent',P)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class AccentTests(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(m.THEMES),10)
 def test_all_genres_have_valid_hex(self):
  for k,v in m.THEMES.items():
   self.assertEqual(len(v),6);int(v,16)
 def test_rms_silence(self):self.assertLess(m.db_rms(np.zeros(16000,dtype='float32'),0),-100)
 def test_rms_speech(self):self.assertGreater(m.db_rms(np.ones(16000,dtype='float32')*.3,0),-15)
 def test_detect_voice_onset(self):
  x=np.zeros(3*m.SR,dtype='float32');x[int(.3*m.SR):int(1.3*m.SR)]=.25
  o=m.detect_onsets(x,[0.0]);self.assertTrue(.2<o[0]<.35)
 def test_does_not_animate_silence(self):
  x=np.zeros(3*m.SR,dtype='float32');self.assertEqual(m.detect_onsets(x,[0.0]),[None])
 def test_ignore_short_sfx(self):
  x=np.zeros(3*m.SR,dtype='float32');x[int(.15*m.SR):int(.18*m.SR)]=.9
  x[int(.5*m.SR):int(1.2*m.SR)]=.2
  o=m.detect_onsets(x,[0.0]);self.assertGreater(o[0],.4)
 def test_filtergraph_no_voice(self):self.assertEqual(m.filtergraph([None]),'null')
 def test_filtergraph_four_steps(self):self.assertEqual(m.filtergraph([.4]).count('drawbox'),4)
 def test_unknown_theme_fails(self):
  with self.assertRaises(ValueError):m.filtergraph([.4],'other')
 def test_no_caption_text_cover(self):self.assertLessEqual(m.CAPTION_TOP+m.ACCENT_HEIGHT,1370)
 def test_filter_has_only_timed_intervals(self):
  f=m.filtergraph([.4,.7]);self.assertEqual(f.count('enable=between'),8)

if __name__=='__main__':unittest.main()
