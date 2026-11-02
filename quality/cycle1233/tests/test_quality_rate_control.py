import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_rate_control import (GENRES, PANEL, FULL_SSIM_FLOOR, PANEL_SSIM_FLOOR,
                                  WIDTH, HEIGHT, FPS, encode, ssim_score)

class QualityRateControlTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES), 10)
    def test_unique_genres(self): self.assertEqual(len(set(GENRES)), 10)
    def test_ai_genre(self): self.assertIn('ai', GENRES)
    def test_video_geometry(self): self.assertEqual((WIDTH, HEIGHT, FPS), (1080, 1920, 30))
    def test_panel_in_frame(self):
        x,y,w,h=PANEL
        self.assertTrue(x>=0 and y>=0 and x+w<=WIDTH and y+h<=HEIGHT)
    def test_quality_floors(self):
        self.assertGreaterEqual(FULL_SSIM_FLOOR, 0.995)
        self.assertGreaterEqual(PANEL_SSIM_FLOOR, 0.99)
    def test_reject_invalid_genre(self):
        with self.assertRaises(ValueError): encode('none', 'out', genre='invalid')
    def test_reject_crf_low(self):
        with self.assertRaises(ValueError): encode('none', 'out', crf=15)
    def test_reject_crf_high(self):
        with self.assertRaises(ValueError): encode('none', 'out', crf=25)
    def test_reject_missing_source(self):
        with self.assertRaises(ValueError): encode('/definitely/not/here', '/tmp/out')
    def test_ssim_regex_parse(self):
        class Fake:
            stderr=b'[Parsed_ssim_0] SSIM Y:0.995 U:0.996 V:0.997 All:0.996000 (24.0)'
        with patch('quality_rate_control.command', return_value=Fake()):
            self.assertEqual(ssim_score('a','b'), 0.996)
    def test_ssim_panel_graph(self):
        class Fake:
            stderr=b'SSIM Y:0.995 U:0.996 V:0.997 All:0.996000 (24.0)'
        with patch('quality_rate_control.command', return_value=Fake()) as m:
            ssim_score('a','b',PANEL)
            self.assertIn('crop=824:694:52:430', m.call_args.args[0][7])

if __name__ == '__main__': unittest.main()
