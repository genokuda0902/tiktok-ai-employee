"""Synthetic tests; never require or commit private video/audio."""
import importlib.util, pathlib, sys, tempfile, unittest
from PIL import Image
p=pathlib.Path(__file__).with_name('verified_totals.py')
s=importlib.util.spec_from_file_location('verified_totals',p)
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)

class ArithmeticContinuity(unittest.TestCase):
    def test_exact_totals(self): self.assertEqual(m.arithmetic(),(46,29))
    def test_reject_incorrect_a(self):
        with self.assertRaises(ValueError):m.arithmetic(totals=(28,29))
    def test_reject_incorrect_b(self):
        with self.assertRaises(ValueError):m.arithmetic(totals=(46,28))
    def test_reject_negative(self):
        with self.assertRaises(ValueError):m.arithmetic(rows=(('4月',-1,8),('5月',16,9),('6月',18,12)))
    def test_ten_genre_rules(self):self.assertEqual(len(m.GENRE_RULES),10)
    def test_only_reviewed_genre(self):
        for g in set(m.GENRE_RULES)-m.REVIEWED:
            with self.assertRaises(PermissionError):m.gate('/missing',g)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):m.gate('/missing','unknown')
    def test_missing_source_fails_closed(self):
        with self.assertRaises(ValueError):m.gate('/missing')
    def test_unapproved_publication_fails(self):
        with self.assertRaises(PermissionError):m.gate('/missing',publish_approved=True)
    def test_frame_dimensions(self):
        self.assertEqual(m.frame(0).size,(1080,1450))
    def test_three_distinct_stages(self):
        self.assertNotEqual(m.frame(0).tobytes(),m.frame(30).tobytes())
        self.assertNotEqual(m.frame(30).tobytes(),m.frame(70).tobytes())
    def test_out_of_range(self):
        with self.assertRaises(ValueError):m.frame(-1)
        with self.assertRaises(ValueError):m.frame(87)
    def test_subtitle_safe_geometry(self):self.assertLess(m.H,1490)
    def test_scene_timing(self):
        self.assertEqual(m.START_FRAME,348);self.assertEqual(m.SCENE_FRAMES,87)

if __name__=='__main__':unittest.main()
