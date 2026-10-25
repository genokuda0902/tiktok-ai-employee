"""Cycle828 regression tests: free, offline, human-review-only."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import cycle828

class Tests(unittest.TestCase):
    def test_ten_genre_colors(self):
        self.assertEqual(len(cycle828.ACCENTS),10)
        for color in cycle828.ACCENTS.values():
            self.assertTrue(cycle828.bgr(color).startswith('&H00'))
    def test_bgr_is_not_rgb(self):
        self.assertEqual(cycle828.bgr('#37C6BE'),'&H00BEC637&')
        self.assertEqual(cycle828.bgr('#FF0000'),'&H000000FF&')
        with self.assertRaises(ValueError):cycle828.bgr('red')
    def test_reuses_speech_timing(self):
        self.assertEqual(sum(cycle828.FRAMES),775)
        self.assertEqual(len(cycle828.FRAMES),8)
    def test_no_auto_post_or_paid_api(self):
        source=Path(cycle828.__file__).read_text()
        for bad in ['tiktok.com/upload','requests.post(', 'api.openai.com']:
            self.assertNotIn(bad,source)
    def test_corrected_caption_layout(self):
        source=Path(cycle828.__file__).read_text()
        self.assertIn('Style: Caption,Noto Sans CJK JP,78,',source)
        self.assertIn(r'\bord0\shad0',source)
        self.assertIn('loudnorm=I=-16:TP=-1.5',source)

if __name__=='__main__':unittest.main()
