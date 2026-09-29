import unittest

from video_engine.production_v2.creative import SCENE_DURATIONS, SCENE_PURPOSES, candidates


class CreativePacingTests(unittest.TestCase):
    def setUp(self):
        self.items = candidates("AI時短", "社会人", "trace-cycle198", "video-cycle198")

    def test_common_pacing_is_twenty_seconds_and_eight_beats(self):
        self.assertEqual(len(SCENE_DURATIONS), 8)
        self.assertAlmostEqual(sum(SCENE_DURATIONS), 20.0)
        self.assertEqual(SCENE_DURATIONS[0], 1.5)

    def test_scene_timeline_is_contiguous_and_fail_closed(self):
        for item in self.items:
            self.assertEqual(item["cut_count"], 8)
            self.assertEqual(item["duration_seconds"], 20.0)
            previous_end = 0.0
            for scene in item["scene_prompts"]:
                self.assertAlmostEqual(scene["start_time"], previous_end)
                self.assertGreater(scene["end_time"], scene["start_time"])
                self.assertEqual(scene["rights_status"], "PENDING")
                previous_end = scene["end_time"]
            self.assertAlmostEqual(previous_end, 20.0)

    def test_scene_purposes_are_explicit_and_genre_independent(self):
        self.assertEqual(SCENE_PURPOSES, ('hook','problem','instruction','processing','result','comparison','proof','cta'))
        for item in self.items:
            self.assertEqual(tuple(s['purpose'] for s in item['scene_prompts']), SCENE_PURPOSES)


if __name__ == "__main__":
    unittest.main()
