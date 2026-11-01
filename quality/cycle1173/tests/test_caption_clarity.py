import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from caption_clarity import DEFAULT_ROI, GENRE_ROI, filter_graph

class CaptionClarityTests(unittest.TestCase):
    def test_roi_within_full_hd_vertical(self):
        x,y,w,h=DEFAULT_ROI
        self.assertTrue(0<=x<x+w<=1080)
        self.assertTrue(0<=y<y+h<=1920)
    def test_filter_localizes(self):
        g=filter_graph()
        self.assertIn('crop=720:180:100:1420',g)
        self.assertIn('overlay=100:1420',g)
        self.assertIn('format=yuv420p',g)
    def test_reject_off_frame(self):
        with self.assertRaises(ValueError): filter_graph(1080,1920,(900,1420,720,180))
    def test_reject_odd_chroma(self):
        with self.assertRaises(ValueError): filter_graph(1080,1920,(101,1420,720,180))
    def test_reject_bad_strength(self):
        with self.assertRaises(ValueError): filter_graph(strength=5)
    def test_all_ten_genres_share_geometry(self):
        self.assertEqual(len(GENRE_ROI), 10)
        self.assertEqual(set(GENRE_ROI.values()), {DEFAULT_ROI})

if __name__=='__main__': unittest.main()
