"""Offline unit tests: no paid services or posting."""
import unittest
from PIL import Image
from photoframe import ACTIONS, FRAME, GENRE_COLORS, PHOTO_BOX, fit_contain, place_photo, validate_genre

class PhotoSafeTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_COLORS),10)
        for key in GENRE_COLORS:
            self.assertTrue(validate_genre(key).startswith("#"))
    def test_eight_action_cues(self):
        self.assertEqual(len(ACTIONS),8)
    def test_preserve_all_shapes(self):
        for width,height in [(956,1000),(640,500),(1200,300),(300,1200)]:
            with self.subTest(size=(width,height)):
                image=Image.new("RGB",(width,height))
                fitted=fit_contain(image)
                self.assertLessEqual(fitted.width,PHOTO_BOX[0])
                self.assertLessEqual(fitted.height,PHOTO_BOX[1])
                self.assertLess(abs(fitted.width/fitted.height-width/height),.003)
    def test_photo_position(self):
        canvas=Image.new("RGB",FRAME)
        result=place_photo(Image.new("RGB",(640,500)),canvas)
        self.assertGreaterEqual(result[0],76)
        self.assertGreaterEqual(result[1],418)
        self.assertLessEqual(result[0]+result[2],76+PHOTO_BOX[0])
        self.assertLessEqual(result[1]+result[3],418+PHOTO_BOX[1])
    def test_invalid_genre(self):
        with self.assertRaises(ValueError): validate_genre("unknown")

if __name__=="__main__": unittest.main()
