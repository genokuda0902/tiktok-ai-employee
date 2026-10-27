import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from cta_path import (WIDTH,HEIGHT,FPS,FRAME_COUNT,START_SEC,POINTS,RAIL_X,CAPTION_TOP,GENRES,POLICY,state_at,overlay_bounds,smoothstep)

class CTAReviewTests(unittest.TestCase):
    def test_portrait_spec(self): self.assertEqual((WIDTH,HEIGHT,FPS),(1080,1920,30))
    def test_ten_genres(self): self.assertEqual(len(GENRES),len(set(GENRES))); self.assertEqual(len(GENRES),10)
    def test_release_fail_closed(self): self.assertFalse(any(POLICY[k] for k in ('publication_approved','automatic_posting','external_upload','paid_service'))); self.assertTrue(POLICY['human_review_required'])
    def test_safe_caption_region(self): self.assertLess(overlay_bounds()[3],CAPTION_TOP)
    def test_no_header_overlap(self): self.assertGreater(overlay_bounds()[1],600)
    def test_all_points_within_bounds(self):
        for x,y in POINTS: self.assertTrue(120<x<230 and 700<y<1200)
    def test_progress_monotonic(self):
        ys=[state_at(i).rail_end_y for i in range(FRAME_COUNT)]
        self.assertEqual(ys,sorted(ys)); self.assertGreater(ys[-1],ys[0]+250)
    def test_three_actions_activated(self): self.assertEqual({state_at(i).active_index for i in range(FRAME_COUNT)}, {0,1,2})
    def test_highlights_visible(self): self.assertTrue(all(max(state_at(i).highlight_alpha[j] for i in range(FRAME_COUNT))>90 for j in range(3)))
    def test_bounds_invalid(self):
        for n in (-1,FRAME_COUNT):
            with self.assertRaises(ValueError): state_at(n)
    def test_smoothstep_clamped(self): self.assertEqual((smoothstep(-1),smoothstep(2)),(0.0,1.0))
    def test_frame_duration(self): self.assertLess(START_SEC+FRAME_COUNT/FPS,23.1)
    def test_separate_from_narration_visualizer(self): self.assertEqual(RAIL_X,106)

if __name__=='__main__': unittest.main()
