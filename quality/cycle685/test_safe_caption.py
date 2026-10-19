import unittest
from PIL import ImageFont
from safe_caption import wrap_caption,validate,SAFE,GENRES
def font(n):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
class Tests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(set(GENRES)),10)
    def test_safe_zone(self): self.assertLessEqual(SAFE[3],1536)
    def test_japanese_visual_text(self):
        for s in ('数字を足す前に、結果を見よう','120＋150＋200＋180＝650','保存して、自分の表で試そう'):
            self.assertTrue(validate(wrap_caption(s,font),font))
    def test_empty_rejected(self):
        with self.assertRaises(ValueError): wrap_caption('',font)
    def test_long_rejected(self):
        with self.assertRaises(ValueError): wrap_caption('長い文章'*250,font)
if __name__=='__main__': unittest.main()
