"""Cycle781 unit tests: safe silence cuts and ten-genre caption remapping."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from pacing import GENRES,remap,segments,stamp,ffmpeg_graph

class PacingTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_remap(self):
        self.assertEqual(remap(7,[(2.5,3),(5.5,6)]),6)
        self.assertEqual(remap(3.4,[(2.5,3)]),2.9)
    def test_reject_time_inside_cut(self):
        with self.assertRaises(ValueError):
            remap(2.75,[(2.5,3)])
    def test_segments(self):
        self.assertEqual(segments([(1,1.5),(2,2.5)],3),[(0,1),(1.5,2),(2.5,3)])
    def test_srt(self):
        self.assertEqual(stamp(62.005),"00:01:02,005")
    def test_concat(self):
        self.assertIn("concat=n=2:v=1:a=1",ffmpeg_graph([(1,1.5)],3))

if __name__=="__main__":
    unittest.main()
