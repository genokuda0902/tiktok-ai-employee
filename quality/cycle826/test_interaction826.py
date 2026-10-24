import sys,unittest
from pathlib import Path
from PIL import ImageChops
sys.path.insert(0,str(Path(__file__).resolve().parent))
import interaction826 as m

class Interaction826Tests(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(m.GENRES),10)
        for genre in m.GENRES:
            with self.subTest(genre=genre):
                m.gate(genre)
                self.assertEqual(m.make_frame(0.5,genre).size,(952,648))
    def test_no_unknown_genre(self):
        with self.assertRaises(ValueError):m.gate('secret')
    def test_no_unsafe_time(self):
        with self.assertRaises(ValueError):m.gate('ai_work',9.0,9.2)
    def test_typed_prompt_changes(self):
        self.assertIsNotNone(ImageChops.difference(m.make_frame(0.04),m.make_frame(0.50)).getbbox())
    def test_output_reveal_changes(self):
        self.assertIsNotNone(ImageChops.difference(m.make_frame(0.60),m.make_frame(0.96)).getbbox())
    def test_restrict_overlay_to_subtitle_safe_box(self):
        x,y,w,h=m.REGION
        self.assertGreaterEqual(y,420)
        self.assertLessEqual(y+h,1190)
    def test_no_private_or_real_app_claim(self):
        self.assertIn('架空',m.PROMPT)
        self.assertNotIn('ChatGPT',m.PROMPT)
    def test_no_false_numeric_result(self):
        self.assertTrue(all('売上' not in s and '%' not in s for s in m.SAMPLE))

if __name__=='__main__':unittest.main()
