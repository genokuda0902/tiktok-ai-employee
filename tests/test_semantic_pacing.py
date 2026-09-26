import unittest

from video_engine.semantic_pacing import DEFAULT_BEATS, release_policy, semantic_pacing


class SemanticPacingTests(unittest.TestCase):
    def test_default_total_and_geometry(self):
        plan = semantic_pacing()
        self.assertEqual(plan["duration"], 12.7)
        self.assertEqual((plan["width"], plan["height"]), (1080, 1920))

    def test_before_after_gets_longer_read_time_than_hook(self):
        d = dict(DEFAULT_BEATS)
        self.assertGreater(d["before_after"], d["hook"])

    def test_wrong_geometry_and_duplicate_beats_fail_closed(self):
        with self.assertRaises(ValueError):
            semantic_pacing(width=720, height=1280)
        with self.assertRaises(ValueError):
            semantic_pacing((("hook", 1.5),) * 8)

    def test_unreadable_or_stalled_beat_fails_closed(self):
        bad = list(DEFAULT_BEATS)
        bad[0] = ("hook", 0.5)
        with self.assertRaises(ValueError):
            semantic_pacing(tuple(bad))

    def test_release_remains_manual_and_rights_gated(self):
        policy = release_policy()
        self.assertTrue(policy["zero_cost"])
        self.assertTrue(policy["human_approval_required"])
        self.assertTrue(policy["rights_approval_required"])
        self.assertFalse(policy["auto_post"])
        self.assertTrue(policy["narration_semantic_sync_must_be_verified_separately"])


if __name__ == "__main__":
    unittest.main()
