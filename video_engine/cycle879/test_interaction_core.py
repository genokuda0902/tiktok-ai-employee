import unittest
from dataclasses import replace
from interaction_core import (build_timeline,validate_timeline,validate_hit_targets,
                              frame_to_seconds,GENRES,SCENE_STATES,State,TOTAL_FRAMES,FPS)

class TimelineTests(unittest.TestCase):
    def test_ten_genres(self):
        for genre in GENRES:
            with self.subTest(genre=genre):self.assertTrue(validate_timeline(genre=genre))
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):validate_timeline(genre='fake')
    def test_exact_total_frames(self):
        t=build_timeline();self.assertEqual(t[0].start,0);self.assertEqual(t[-1].end,691)
        self.assertEqual(sum(s.end-s.start for s in t),691)
    def test_twenty_distinct_states(self):self.assertEqual(len(build_timeline()),20)
    def test_eight_scenes(self):self.assertEqual(set(s.scene for s in build_timeline()),set(range(1,9)))
    def test_animated_scenes(self):
        for s in [1,2,4,5,7]:self.assertGreater(sum(x.scene==s for x in build_timeline()),1)
    def test_gap_rejected(self):
        t=list(build_timeline());t[1]=replace(t[1],start=t[1].start+1)
        with self.assertRaises(ValueError):validate_timeline(t)
    def test_overlap_rejected(self):
        t=list(build_timeline());t[1]=replace(t[1],start=t[1].start-1)
        with self.assertRaises(ValueError):validate_timeline(t)
    def test_empty_rejected(self):
        with self.assertRaises(ValueError):validate_timeline([])
    def test_short_rejected(self):
        with self.assertRaises(ValueError):validate_timeline(build_timeline()[:-1])
    def test_bad_stage_rejected(self):
        t=list(build_timeline());t[1]=replace(t[1],stage=5)
        with self.assertRaises(ValueError):validate_timeline(t)
    def test_scene_reverse_rejected(self):
        t=list(build_timeline());t[2]=replace(t[2],scene=0)
        with self.assertRaises(ValueError):validate_timeline(t)
    def test_hit_targets_safe(self):self.assertTrue(validate_hit_targets())
    def test_hit_target_overlap_rejected(self):
        with self.assertRaises(ValueError):validate_hit_targets({'bad':(100,1400,700,1500)})
    def test_frames_to_seconds(self):self.assertEqual(frame_to_seconds(691),691/30)
    def test_invalid_frame_rejected(self):
        with self.assertRaises(ValueError):frame_to_seconds(-1)
    def test_scene_time_positive(self):
        for s in build_timeline():self.assertGreater(s.end-s.start,0)

if __name__=='__main__':unittest.main()
