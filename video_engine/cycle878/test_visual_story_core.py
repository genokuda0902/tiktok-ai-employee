"""No-dependency regression tests for original synthetic visual examples."""
import unittest
from dataclasses import replace
from visual_story_core import (
    GENRES, SCENES, DEMO_FOCUS, MAIN_VISUAL, CAPTION_SAFE,
    validate_story, inside,
)

class StoryTests(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for key in GENRES:
            self.assertTrue(validate_story(genre=key))

    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):
            validate_story(genre="unknown")

    def test_empty_visual_explanation_rejected(self):
        scenes=list(SCENES)
        scenes[2]=replace(scenes[2],proof_type="")
        with self.assertRaises(ValueError):
            validate_story(scenes=scenes)

    def test_scene_gap_rejected(self):
        scenes=list(SCENES)
        scenes[2]=replace(scenes[2],start=6.1)
        with self.assertRaises(ValueError):
            validate_story(scenes=scenes)

    def test_scene_overlap_rejected(self):
        scenes=list(SCENES)
        scenes[2]=replace(scenes[2],start=5.7)
        with self.assertRaises(ValueError):
            validate_story(scenes=scenes)

    def test_caption_collision_rejected(self):
        with self.assertRaises(ValueError):
            validate_story(focus=[("bad",10,11,(50,1400,900,1550))])

    def test_focus_timing_rejected(self):
        with self.assertRaises(ValueError):
            validate_story(focus=[("bad",11,10,(50,600,900,900))])

    def test_focus_inside_visual(self):
        for _,_,_,rect in DEMO_FOCUS:
            self.assertTrue(inside(rect,MAIN_VISUAL))

    def test_final_duration(self):
        self.assertAlmostEqual(SCENES[-1].end,691/30)

    def test_caption_separation(self):
        self.assertLess(MAIN_VISUAL[3],CAPTION_SAFE[1])

    def test_scene_uniqueness(self):
        self.assertEqual(len(set(x.key for x in SCENES)),8)

    def test_scene_has_concrete_proof(self):
        self.assertTrue(all(x.proof_type for x in SCENES))

if __name__ == "__main__":
    unittest.main()
