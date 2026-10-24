"""Offline regression tests: genre palette, hook, TikTok UI safe region, audio captions, publication gate."""
import importlib.util, pathlib, tempfile, unittest
from PIL import Image, ImageChops
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cycle826',HERE/'cycle826.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Cycle826Tests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.COLORS),10)
        self.assertEqual(set(m.COLORS),set(m.rail.PALETTES))
    def test_duration(self):
        self.assertEqual(sum(m.FRAMES),775)
        self.assertEqual(len(m.FRAMES),8)
    def test_24_subtitle_states(self):
        with tempfile.TemporaryDirectory() as t:
            txt=m.make_ass(pathlib.Path(t)).read_text()
        self.assertEqual(txt.count('Dialogue: 0,'),24)
        self.assertIn(r'\pos(540,1540)',txt)
        self.assertIn('JP,65,',txt)
    def test_caption_matches_voice_script(self):
        self.assertTrue(all(''.join(x)==y for x,y in zip(m.PHRASES,m.SPEECH)))
    def test_hook_is_visible_and_not_identical_to_old_screen(self):
        new=m.screen_content(0,m.COLORS['ai_work'])
        old=m.screen_content(1,m.COLORS['ai_work'])
        self.assertIsNotNone(ImageChops.difference(new,old).getbbox())
        self.assertEqual(new.getpixel((195,220)),(251,234,230))
        self.assertEqual(new.getpixel((580,220)),(227,246,242))
    def test_action_rail_avoids_bottom_and_right_ui(self):
        im=m.rail.apply_action_rail(Image.new('RGB',(1080,1920)),0)
        self.assertEqual(im.getpixel((400,1840)),(13,36,52,255))
        self.assertEqual(im.getpixel((1010,1450)),(13,36,52,255))
    def test_eight_distinct_actions(self):
        self.assertEqual(len(set(m.ACTION)),8)
    def test_deterministic_hook(self):
        self.assertIsNone(ImageChops.difference(m.screen_content(0,m.COLORS['ai_work']),m.screen_content(0,m.COLORS['ai_work'])).getbbox())
    def test_review_only_no_network_publish(self):
        code=(HERE/'cycle826.py').read_text()
        self.assertIn("'posting_allowed':False",code)
        self.assertNotIn('requests.post(',code)
        self.assertNotIn('tiktok.com/upload',code)

if __name__=='__main__':unittest.main()