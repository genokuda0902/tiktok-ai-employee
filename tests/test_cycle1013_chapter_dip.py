import importlib.util
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/'tools/quality/cycle1013_chapter_dip.py'
spec=importlib.util.spec_from_file_location('dip',P)
dip=importlib.util.module_from_spec(spec)
spec.loader.exec_module(dip)

class TestChapterDip(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(dip.GENRES),10)
    def test_chapter_dedupe(self):
        chapters={'chapters':[{'start_time':'0'},{'start_time':'2.633'},
            {'start_time':'5.800'},{'start_time':'5.800'},{'start_time':'22.5'}]}
        self.assertEqual(dip.chapter_cuts(chapters,22.5),[2.633,5.8])
    def test_expression(self):
        e=dip.brightness_expr([2.633,5.8])
        self.assertIn('abs(t-2.633)',e)
        self.assertIn('abs(t-5.800)',e)
        self.assertIn('max(',e)
    def test_no_cuts(self):
        self.assertEqual(dip.brightness_expr([]),'0')
    def test_reject_strength(self):
        with self.assertRaises(ValueError): dip.brightness_expr([2],strength=.5)
    def test_reject_window(self):
        with self.assertRaises(ValueError): dip.brightness_expr([2],window=.02)
    def test_reject_genre(self):
        with self.assertRaises(ValueError): dip.render('a','b',genre='unknown')
    def test_reject_overwrite(self):
        with self.assertRaises(ValueError): dip.render('/tmp/a','/tmp/a')

if __name__=='__main__': unittest.main()
