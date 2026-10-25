import unittest
from photo_dissolve import (GENRES,POLICY,SCENE_LENGTHS,BOUNDARIES,
    TRANSITION_FRAMES,PHOTO_BOX,easing,timeline,check_manifest)

class PhotoDissolveTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
    def test_review_policy(self):
        check_manifest(POLICY,'ai_work')
        with self.assertRaises(ValueError):
            check_manifest({**POLICY,'automatic_posting':True},'ai_work')
        with self.assertRaises(ValueError):
            check_manifest({**POLICY,'contains_personal_data':True},'ai_work')
        with self.assertRaises(ValueError):
            check_manifest(POLICY,'unknown')
    def test_frame_exact(self):
        segments=timeline()
        self.assertEqual(sum(x[2] for x in segments),691)
        self.assertEqual(sum(x[0]=='dissolve' for x in segments),7)
    def test_smooth_blend(self):
        alphas=[easing(i) for i in range(TRANSITION_FRAMES)]
        self.assertTrue(all(0<=x<=1 for x in alphas))
        self.assertTrue(all(x<y for x,y in zip(alphas,alphas[1:])))
        self.assertAlmostEqual(alphas[0]+alphas[-1],1,places=9)
    def test_boundaries(self):
        self.assertEqual(BOUNDARIES,(89,170,249,336,422,511,588))
    def test_photo_region(self):
        self.assertEqual(PHOTO_BOX,(30,350,1050,1300))
    def test_invalid_timelines(self):
        with self.assertRaises(ValueError):timeline((4,4),12)
        with self.assertRaises(ValueError):easing(-1)
    def test_eight_scenes(self):
        self.assertEqual(len(SCENE_LENGTHS),8)

if __name__=='__main__':unittest.main()
