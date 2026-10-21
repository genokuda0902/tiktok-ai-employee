import unittest
from cta_scene import card, validate, PHASES, START, END, TOTAL

class TestScene(unittest.TestCase):
    def test_timeline(self):
        self.assertEqual((START, END, TOTAL),(729,819,819))
        self.assertEqual(sum(PHASES),90)
    def test_rendered_artwork(self):
        for i in range(3):
            img=card(i)
            self.assertEqual(img.size,(1080,1920))
            self.assertEqual(img.mode,'RGB')
    def test_fail_closed(self):
        with self.assertRaises(ValueError):validate('unverified')

if __name__=='__main__':unittest.main()
