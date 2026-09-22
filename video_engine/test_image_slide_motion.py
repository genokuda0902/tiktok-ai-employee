import unittest

from image_slide_motion import (
    DEFAULT_EVENTS,
    MOTION_PROFILES,
    comparison_filter,
    event_manifest_filter,
    hook_hierarchy_filter,
    interaction_filter,
    interactive_motion_filter,
    motion_filter,
    semantic_reaction_filter,
)


class ImageSlideMotionTests(unittest.TestCase):
    def test_profiles_are_reusable(self):
        self.assertGreaterEqual(len(MOTION_PROFILES), 4)
        for i in range(12):
            value = motion_filter(i)
            self.assertIn("crop=1080:1920", value)
            self.assertIn("scale=", value)

    def test_interaction_filter_has_cursor_and_click_pulse(self):
        value = interaction_filter()
        self.assertIn("drawbox=", value)
        self.assertIn("enable=", value)

    def test_event_manifest_uses_explicit_timeline_not_periodic_reaction(self):
        value = event_manifest_filter(DEFAULT_EVENTS)
        self.assertIn("between(t,0.000,0.560)", value)
        self.assertIn("between(t,6.500,7.060)", value)
        self.assertIn("between(t,13.000,13.560)", value)
        self.assertNotIn("mod(t,2.5)", value)
        self.assertEqual(value.count("drawbox="), 12)

    def test_event_manifest_rejects_invalid_or_unsorted_events(self):
        with self.assertRaises(ValueError):
            event_manifest_filter(({"start": 2, "processing": .5, "result": 1.2}, {"start": 1, "processing": .5, "result": 1.2}))
        with self.assertRaises(ValueError):
            event_manifest_filter(({"start": 0, "processing": .8, "result": .4},))

    def test_hook_hierarchy_is_genre_copy_driven(self):
        value = hook_hierarchy_filter("問題提起", "便益", "/tmp/font.ttc")
        self.assertIn("問題提起", value)
        self.assertIn("便益", value)
        self.assertIn("between(t,0,2.8)", value)
        self.assertIn("between(t,2.8,5.8)", value)

    def test_hook_hierarchy_fails_closed(self):
        with self.assertRaises(ValueError):
            hook_hierarchy_filter("", "便益", "/tmp/font.ttc")
        with self.assertRaises(ValueError):
            hook_hierarchy_filter("問題", "", "/tmp/font.ttc")

    def test_comparison_beat_is_copy_driven_and_timed(self):
        value = comparison_filter("手作業", "AIで短縮", "/tmp/font.ttc", 8.0, 12.0)
        self.assertIn("BEFORE", value)
        self.assertIn("AFTER", value)
        self.assertIn("手作業", value)
        self.assertIn("AIで短縮", value)
        self.assertIn("between(t,8.000,12.000)", value)

    def test_comparison_beat_fails_closed(self):
        with self.assertRaises(ValueError):
            comparison_filter("", "改善", "/tmp/font.ttc")
        with self.assertRaises(ValueError):
            comparison_filter("現状", "改善", "/tmp/font.ttc", 12.0, 8.0)
        with self.assertRaises(ValueError):
            comparison_filter("現状", "改善", "/tmp/font.ttc", width=720, height=1280)

    def test_semantic_reaction_remains_backward_compatible(self):
        value = semantic_reaction_filter()
        self.assertIn("mod(t,2.5)", value)

    def test_combined_filter_uses_manifest_reactions(self):
        value = interactive_motion_filter(2)
        self.assertIn("crop=1080:1920", value)
        self.assertIn("between(t,6.500,7.060)", value)
        self.assertGreaterEqual(value.count("drawbox="), 14)

    def test_fail_closed_for_non_portrait_target(self):
        with self.assertRaises(ValueError):
            motion_filter(0, 720, 1280)
        with self.assertRaises(ValueError):
            interaction_filter(720, 1280)
        with self.assertRaises(ValueError):
            event_manifest_filter(DEFAULT_EVENTS, 720, 1280)
        with self.assertRaises(ValueError):
            hook_hierarchy_filter("問題", "便益", "/tmp/font.ttc", 720, 1280)
        with self.assertRaises(ValueError):
            semantic_reaction_filter(720, 1280)
        with self.assertRaises(ValueError):
            interactive_motion_filter(0, 720, 1280)


if __name__ == "__main__":
    unittest.main()
