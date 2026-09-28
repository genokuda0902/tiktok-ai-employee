import unittest

from video_engine.semantic_gap_compaction import (
    Interval,
    plan_excess_silence_cuts,
    posting_policy,
)


class SemanticGapCompactionTests(unittest.TestCase):
    def test_cycle44_measured_gaps_are_compacted_without_removing_all_pause(self):
        silences = [
            Interval(1.538792, 3.9825),
            Interval(6.322312, 8.083208),
            Interval(9.950521, 12.139333),
            Interval(14.088125, 16.086688),
            Interval(18.540771, 20.0),
        ]
        cuts = plan_excess_silence_cuts(silences, 20.0)
        self.assertEqual(len(cuts), 5)
        self.assertAlmostEqual(cuts[0].start, 1.813792, places=6)
        self.assertAlmostEqual(cuts[0].end, 3.7075, places=6)
        removed = sum(c.duration for c in cuts)
        self.assertAlmostEqual(removed, 7.281, places=3)

    def test_short_natural_pause_is_not_cut(self):
        self.assertEqual(plan_excess_silence_cuts([Interval(1.0, 1.4)], 3.0), [])

    def test_invalid_intervals_fail_closed(self):
        with self.assertRaises(ValueError):
            plan_excess_silence_cuts([Interval(2.0, 1.0)], 3.0)

    def test_manual_posting_only(self):
        policy = posting_policy()
        self.assertTrue(policy["zero_cost"])
        self.assertTrue(policy["human_approval_required"])
        self.assertFalse(policy["auto_post"])


if __name__ == "__main__":
    unittest.main()
