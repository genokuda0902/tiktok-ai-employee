import sys,unittest
from pathlib import Path
from PIL import ImageChops
sys.path.insert(0,str(Path(__file__).resolve().parent))
import apply828 as m

class Apply828Tests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRES),10)
        for g in m.GENRES:
            with self.subTest(genre=g):
                self.assertTrue(m.validate(g))
                self.assertEqual(m.frame(.5,g).size,(952,648))
    def test_bad_genre(self):
        with self.assertRaises(ValueError):m.validate('unknown')
    def test_scene_range_locked(self):
        with self.assertRaises(ValueError):m.validate(start=15)
    def test_safe_subtitle_region(self):
        self.assertLessEqual(m.Y+m.H,1190)
    def test_four_action_stages(self):
        a,b,c,d=(m.frame(p) for p in (.04,.3,.6,.98))
        for x,y in ((a,b),(b,c),(c,d)):
            self.assertIsNotNone(ImageChops.difference(x,y).getbbox())
    def test_no_unverified_results(self):
        self.assertIn('架空',m.NOTICE)
        self.assertNotIn('売上',m.NOTICE)
        self.assertNotIn('%',m.NOTICE)
    def test_no_auto_post_or_approval(self):
        src=Path(m.__file__).read_text()
        self.assertIn("'auto_post':False",src)
        self.assertIn("'publication_approved':False",src)

if __name__=='__main__':unittest.main()
