import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from scene_wipe import (GENRE_ACCENTS, DEFAULT_CUTS, POLICY, smoothstep,
                        reveal_fraction, validate_settings)

class TransitionTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRE_ACCENTS),10)
    def test_unique_genres(self): self.assertEqual(len(set(GENRE_ACCENTS)),10)
    def test_rgb_bounds(self):
        for bgr in GENRE_ACCENTS.values():
            self.assertEqual(len(bgr),3)
            self.assertTrue(all(isinstance(x,int) and 0<=x<=255 for x in bgr))
    def test_seven_cuts(self): self.assertEqual(DEFAULT_CUTS,(87,174,261,348,435,522,609))
    def test_smoothstep(self):
        self.assertEqual(smoothstep(-1),0)
        self.assertEqual(smoothstep(2),1)
        self.assertAlmostEqual(smoothstep(.5),.5)
    def test_progress_increasing(self):
        x=[reveal_fraction(i,9) for i in range(9)]
        self.assertTrue(all(a<b for a,b in zip(x,x[1:])))
        self.assertGreater(x[0],0)
        self.assertLess(x[-1],1)
    def test_invalid_step(self):
        with self.assertRaises(ValueError): reveal_fraction(9,9)
    def test_valid_settings(self): self.assertTrue(validate_settings('ai_work',DEFAULT_CUTS,9,1460,1920,691))
    def test_no_overlapping_wipes(self):
        with self.assertRaises(ValueError):validate_settings('ai_work',(87,91),9,1460,1920,691)
    def test_no_unknown_genre(self):
        with self.assertRaises(ValueError):validate_settings('unknown',DEFAULT_CUTS,9,1460,1920,691)
    def test_subtitle_protected(self):
        with self.assertRaises(ValueError):validate_settings('ai_work',DEFAULT_CUTS,9,1950,1920,691)
    def test_policy(self): self.assertIn('PUBLICATION_NOT_APPROVED',POLICY)
    def test_wipe_preserves_footer_if_numpy_available(self):
        try:
            import numpy as np
            from scene_wipe import wipe_frame
        except ImportError:
            self.skipTest('numpy not installed in CI')
        a=np.full((300,240,3),220,dtype=np.uint8)
        b=np.full((300,240,3),10,dtype=np.uint8)
        result=wipe_frame(a,b,4,9,220,GENRE_ACCENTS['ai_work'])
        self.assertTrue(np.array_equal(result[220:],a[220:]))
        self.assertFalse(np.array_equal(result[:220],a[:220]))

if __name__=='__main__':unittest.main()
