import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"quality/cycle487"))
import tts,build
class ReviewTests(unittest.TestCase):
 def test_six_voice_scripts(self):
  self.assertEqual(len(tts.SCRIPTS),6)
  for s in tts.SCRIPTS:self.assertTrue(any("あ"<=c<="龥" for c in s))
 def test_dimensions(self):self.assertEqual((build.W,build.H,build.FPS),(1080,1920,30))
 def test_fail_closed(self):
  from unittest.mock import patch
  with patch("shutil.which",return_value=None):
   with self.assertRaises(RuntimeError):tts.synthesize("/tmp/voice_should_not_exist")
if __name__=="__main__":unittest.main()
