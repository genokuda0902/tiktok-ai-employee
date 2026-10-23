import unittest
from tts_ci import TEXTS,TITLES,PALETTE
class TestCycle802Contract(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(PALETTE),10)
    def test_unique_colors(self):self.assertEqual(len(set(PALETTE.values())),10)
    def test_eight_scenes(self):self.assertEqual(len(TEXTS),8)
    def test_eight_titles(self):self.assertEqual(len(TITLES),8)
    def test_japanese_voice_script(self):
        self.assertTrue(all(any(ord(ch)>127 for ch in s) for s in TEXTS))
    def test_no_auto_post(self):
        from pathlib import Path
        code=(Path(__file__).parent/"tts_ci.py").read_text()
        self.assertNotIn("upload_video(",code)
if __name__=="__main__":unittest.main()
