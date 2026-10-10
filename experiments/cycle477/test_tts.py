"""Static tests for native Japanese TTS contract."""
import unittest
from japanese_tts import LINES,DURATIONS
class TestTTS(unittest.TestCase):
 def test_six_lines(self):self.assertEqual(len(LINES),6)
 def test_total_duration(self):self.assertAlmostEqual(sum(DURATIONS),18)
 def test_japanese(self):self.assertTrue(all(any('\u3040'<=c<='\u9fff' for c in line) for line in LINES))
 def test_no_real_names(self):self.assertTrue(all('奥田' not in line for line in LINES))
if __name__=='__main__':unittest.main()
