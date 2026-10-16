import unittest
from render import GENRES,SCENES,check,draw
class Cycle629Tests(unittest.TestCase):
    def test_genres(self):
        for g in GENRES:self.assertTrue(check(g))
    def test_genre_count(self):self.assertEqual(len(GENRES),10)
    def test_reject_unapproved(self):
        with self.assertRaises(ValueError):check(rights="UNKNOWN")
        with self.assertRaises(ValueError):check(status="APPROVED")
    def test_evidence_math(self):
        self.assertEqual(sum((120,150,200,250)),720)
    def test_caption_every_scene(self):
        self.assertEqual(len(SCENES),4)
        for title,cap,rows in SCENES:
            self.assertTrue(title and cap and rows)
    def test_frame_sizes(self):
        for i in range(4):self.assertEqual(draw(i).size,(540,960))
if __name__=="__main__":unittest.main()
