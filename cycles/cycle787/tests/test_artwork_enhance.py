import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from artwork_enhance import PRESETS, ROI, filter_graph

class TestArtworkEnhance(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(PRESETS), 10)
    def test_roi_excludes_captions(self):
        self.assertEqual(ROI, (42, 378, 846, 662))
        self.assertLessEqual(ROI[1]+ROI[3], 1050)
    def test_graph_has_detail_processing(self):
        graph = filter_graph()
        self.assertIn("eq=gamma=", graph)
        self.assertIn("unsharp=", graph)
        self.assertIn("overlay=42:378", graph)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):
            filter_graph("not-a-genre")
    def test_invalid_roi(self):
        with self.assertRaises(ValueError):
            filter_graph(roi=(0, 1000, 100, 100))
    def test_caption_not_touched(self):
        self.assertNotIn("subtitles=", filter_graph())

if __name__ == "__main__":
    unittest.main()
