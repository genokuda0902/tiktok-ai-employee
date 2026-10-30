import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'source'/'scene2_clarity.py'
spec=importlib.util.spec_from_file_location('scene2',SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Scene2Tests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(m.GENRES),10)
    def test_three_cards_for_each_genre(self):
        for genre in m.GENRES:
            with self.subTest(genre=genre):
                f=m.filter_graph(genre,2.9,5.8)
                self.assertEqual(f.count('w=868:h=192'),3)
                self.assertIn('y=990',f)
    def test_caption_safe_area(self):
        s=m.filter_graph('ai_work',2.9,5.8)
        self.assertIn('y=1327',s)
        self.assertNotIn('y=1490',s)
        self.assertNotIn('y=1520',s)
    def test_three_reveal_times(self):
        s=m.filter_graph('ai_work',2.9,5.8)
        for v in ('3.080','3.760','4.440'):self.assertIn(v,s)
    def test_reject_bad_genre(self):
        with self.assertRaises(ValueError):m.filter_graph('invalid',2.9,5.8)
    def test_reject_bad_time(self):
        with self.assertRaises(ValueError):m.filter_graph('ai_work',5.8,2.9)
    def test_reject_unescaped_text(self):
        with self.assertRaises(ValueError):m.escape('abc:bad')
    def test_review_gate(self):
        with self.assertRaises(ValueError):m.render('missing','out','report','ai_work','0'*64,False)
    def test_missing_source_fails(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):m.render(Path(d)/'missing',Path(d)/'out',Path(d)/'report','ai_work','0'*64,True)
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_text('x')
            with self.assertRaises(ValueError):m.render(p,p,Path(d)/'report','ai_work','0'*64,True)

if __name__=='__main__':unittest.main()
