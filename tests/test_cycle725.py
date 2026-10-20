import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import cycle725_render as c
import cycle720_render as base

class TestCycle725(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base.SCENES[0]=(c.HOOK,c.HOOK_VOICE,"before")
    def test_genres(self):
        self.assertEqual(len(set(c.GENRES)),10)
    def test_math(self):
        self.assertEqual(sum(c.SALES),65)
    def test_voice(self):
        self.assertIn("六十五万円",c.HOOK_VOICE)
    def test_captions(self):
        for _,spoken,_ in base.SCENES:
            lines=c.wrap_pixels(spoken,base.font(c.CAPTION_FONT))
            self.assertEqual("".join(lines),spoken)
            self.assertLessEqual(len(lines),2)
    def test_overflow(self):
        with self.assertRaises(ValueError):
            c.wrap_pixels("あ"*100,base.font(c.CAPTION_FONT))
    def test_empty(self):
        with self.assertRaises(ValueError):
            c.wrap_pixels("",base.font(c.CAPTION_FONT))
    def test_contract(self):
        self.assertTrue(c.validate_contract())

if __name__=="__main__":unittest.main()
