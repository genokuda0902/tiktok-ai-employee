import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from specificity_component import *
class TestSpecificity(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES: self.assertEqual(render_art(2.6,g).size,(W,H))
    def test_timing(self): self.assertLess(BEATS[-1],87/30)
    def test_changes(self): self.assertNotEqual(render_art(.1).tobytes(),render_art(2.7).tobytes())
    def test_typing(self):
        self.assertEqual(visible_chars(.1),0)
        self.assertEqual(visible_chars(2.6),len(SPECIFIC))
    def test_invalid(self):
        with self.assertRaises(ValueError): render_art(1,'invalid')
    def test_smooth(self):
        self.assertEqual(smooth(-1),0)
        self.assertEqual(smooth(2),1)
    def test_no_personal_data(self): self.assertNotIn('奥田',VAGUE+SPECIFIC)
if __name__=='__main__': unittest.main()
