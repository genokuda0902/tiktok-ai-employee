import unittest
from unittest.mock import patch
from quality.cycle488.ci_tts import SCRIPTS,GENRES,locate
class VoiceGateTest(unittest.TestCase):
    def test_six_lines(self): self.assertEqual(len(SCRIPTS),6)
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_japanese_text(self): self.assertTrue(all(any(ord(c)>127 for c in s) for s in SCRIPTS))
    def test_missing_binary_fails_closed(self):
        with patch("shutil.which",return_value=None):
            with self.assertRaisesRegex(RuntimeError,"JAPANESE_TTS_UNAVAILABLE"): locate()
if __name__=="__main__": unittest.main()
