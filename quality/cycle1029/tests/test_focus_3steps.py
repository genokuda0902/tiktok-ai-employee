import importlib.util
import unittest
from pathlib import Path

FILE=Path(__file__).resolve().parents[1]/'code'/'focus_3steps.py'
spec=importlib.util.spec_from_file_location('focus_3steps',FILE)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class FocusTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(mod.GENRES),10)
        self.assertEqual(len(set(mod.COLORS)),10)
    def test_graph_for_all_genres(self):
        for g in mod.GENRES:
            with self.subTest(genre=g):
                graph=mod.filtergraph(g)
                self.assertEqual(graph.count('drawbox='),6)
                self.assertIn('format=yuv420p',graph)
                self.assertIn(mod.COLORS[g],graph)
    def test_three_nonoverlapping_stages(self):
        win=mod.stage_windows(19.767,22.5)
        self.assertEqual(len(win),3)
        self.assertEqual(win[0][0],19.767)
        self.assertEqual(win[-1][-1],22.5)
        self.assertEqual(win[0][1],win[1][0])
    def test_caption_and_header_protected(self):
        for x,y,w,h in mod.DEFAULT_BOXES:
            self.assertGreater(y,380)
            self.assertLess(y+h,1170)
        self.assertNotIn('crop=',mod.filtergraph())
    def test_invalid_box_outside_safe_area(self):
        with self.assertRaises(ValueError):
            mod.validate_boxes(((118,1200,200,100),)+mod.DEFAULT_BOXES[1:])
    def test_overlapping_boxes_rejected(self):
        with self.assertRaises(ValueError):
            mod.validate_boxes((mod.DEFAULT_BOXES[0],mod.DEFAULT_BOXES[0],mod.DEFAULT_BOXES[2]))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):
            mod.filtergraph('unlisted')
    def test_too_short_stage(self):
        with self.assertRaises(ValueError):
            mod.stage_windows(1,2)
    def test_original_media_missing(self):
        with self.assertRaises(FileNotFoundError):
            mod.render('/this/file/does/not/exist.mp4','/tmp/no.mp4')

if __name__=='__main__':unittest.main()
