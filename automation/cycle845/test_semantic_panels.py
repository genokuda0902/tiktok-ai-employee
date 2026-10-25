import unittest
from PIL import ImageChops
from semantic_panels import GENRES, POLICY, FRAMES, SCENES, board, validate, W, H

class TestSemanticPanels(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES: validate(genre,POLICY)
    def test_review_only(self):
        for k in POLICY:
            unsafe=dict(POLICY);unsafe[k]=not POLICY[k]
            with self.assertRaises(ValueError): validate('ai_work',unsafe)
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError): validate('unknown',POLICY)
    def test_timeline(self):
        self.assertEqual(len(FRAMES),8)
        self.assertEqual(sum(FRAMES),691)
    def test_native_assets(self):
        for i in range(8):
            img=board(i)
            self.assertEqual(img.size,(W,H))
            self.assertEqual(img.mode,'RGBA')
            self.assertGreater(img.getpixel((100,100))[3],0)
    def test_distinct_scenes(self):
        for i in range(7):
            diff=ImageChops.difference(board(i).convert('RGB'),board(i+1).convert('RGB'))
            self.assertIsNotNone(diff.getbbox())
    def test_scenes_have_three_steps(self):
        self.assertTrue(all(len(s[3])==3 for s in SCENES))

if __name__=='__main__': unittest.main()
