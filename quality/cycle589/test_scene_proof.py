import unittest
from dataclasses import replace
from scene_proof import Proof, GENRES, validate, render_frame, W, H, FPS, SECONDS
class ProofTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES: self.assertTrue(validate(replace(Proof(), genre=genre)))
    def test_numeric_integrity(self):
        self.assertEqual(sum(Proof().values),720)
        with self.assertRaises(ValueError): validate(replace(Proof(), claimed_total=277))
    def test_negative_rejected(self):
        with self.assertRaises(ValueError): validate(replace(Proof(), values=(120,-1,200,250)))
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError): validate(replace(Proof(), genre='unknown'))
    def test_geometry_and_frames(self):
        self.assertEqual((W,H,FPS,SECONDS),(1080,1920,30,3))
        for i in (0,30,60,89): self.assertEqual(render_frame(i).size,(W,H))
    def test_subtitle_length(self):
        with self.assertRaises(ValueError): validate(replace(Proof(), subtitle='長文'*30))
if __name__=='__main__': unittest.main()
