import unittest
from tools.quality.cycle1005_after_card import make_patch, GENRES, PATCH_BOX, CAPTION_TOP, COPY

class PatchTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES:
            im=make_patch(g)
            self.assertEqual(im.size,(1080,1920))
            self.assertEqual(im.getpixel((200,960))[3],255)
    def test_protected_caption(self):
        im=make_patch()
        self.assertLess(PATCH_BOX[3],CAPTION_TOP)
        self.assertEqual(im.getpixel((500,1350))[3],0)
        self.assertEqual(im.getpixel((500,200))[3],0)
    def test_copy_and_layout(self):
        self.assertIn('3行',COPY[1])
        im=make_patch()
        self.assertNotEqual(im.getpixel((160,1050)),im.getpixel((160,1100)))
    def test_unknown_genre_fails(self):
        with self.assertRaises(ValueError):make_patch('not_a_genre')
if __name__=='__main__': unittest.main()
