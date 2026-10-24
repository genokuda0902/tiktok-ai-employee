import sys,unittest
from pathlib import Path
from PIL import ImageChops
sys.path.insert(0,str(Path(__file__).resolve().parent))
import proof827 as m

class Proof827Tests(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(m.GENRES),10)
        for g in m.GENRES:
            with self.subTest(genre=g):
                self.assertTrue(m.validate(g))
                self.assertEqual(m.make_frame(.5,g).size,(952,648))
    def test_bad_genre_fails(self):
        with self.assertRaises(ValueError):m.validate('not_a_genre')
    def test_bad_timing_fails(self):
        with self.assertRaises(ValueError):m.validate('ai_work',12.,12.1)
    def test_source_values_are_computed(self):
        self.assertEqual(sum(m.SOURCE),m.EXPECTED)
        with self.assertRaises(ValueError):m.validate(source=(12,9))
    def test_no_private_data_or_real_app_claim(self):
        self.assertIn('架空',m.DISCLAIMER)
        self.assertIn('実在のサービス画面ではありません',m.DISCLAIMER)
    def test_subtitle_safe_region(self):
        x,y,w,h=m.prior.REGION
        self.assertLessEqual(y+h,1190)
    def test_three_visual_phases(self):
        a,b,c=(m.make_frame(p) for p in (.1,.5,.95))
        self.assertIsNotNone(ImageChops.difference(a,b).getbbox())
        self.assertIsNotNone(ImageChops.difference(b,c).getbbox())
    def test_no_unverified_revenue_claim(self):
        self.assertNotIn('売上',m.DISCLAIMER)
        self.assertNotIn('%',m.DISCLAIMER)

if __name__=='__main__':unittest.main()
