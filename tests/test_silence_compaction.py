import unittest

from video_engine.silence_compaction import keep_ranges, removal_ranges, sync_contract


class SilenceCompactionTests(unittest.TestCase):
    def test_long_gaps_are_capped_without_removing_short_pauses(self):
        silences = [(1.56, 4.01), (4.75, 5.19), (6.34, 8.10)]
        cuts = removal_ranges(silences, max_pause=0.45, duration=20.0)
        self.assertEqual(len(cuts), 2)
        self.assertAlmostEqual(cuts[0][0], 2.01, places=2)
        self.assertAlmostEqual(cuts[0][1], 4.01, places=2)
        self.assertAlmostEqual(cuts[1][0], 6.79, places=2)

    def test_keep_ranges_preserve_order(self):
        keep = keep_ranges([(2.0, 4.0), (7.0, 8.0)], duration=10.0)
        self.assertEqual(keep, [(0.0, 2.0), (4.0, 7.0), (8.0, 10.0)])

    def test_invalid_or_overaggressive_settings_fail_closed(self):
        with self.assertRaises(ValueError):
            removal_ranges([(1.0, 0.5)], duration=20.0)
        with self.assertRaises(ValueError):
            removal_ranges([(1.0, 2.0)], max_pause=0.1, duration=20.0)

    def test_safety_contract(self):
        c = sync_contract()
        self.assertTrue(c["cut_video_and_audio_together"])
        self.assertTrue(c["caption_copy_unchanged"])
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])


if __name__ == "__main__":
    unittest.main()
