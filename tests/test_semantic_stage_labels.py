import unittest
from video_engine.semantic_stage_labels import Stage, validate_stages, ffmpeg_overlay_filters, posting_policy


class SemanticStageLabelsTest(unittest.TestCase):
    def setUp(self):
        self.stages = [
            Stage("HOOK", 0.0, 2.0),
            Stage("課題", 2.0, 4.4),
            Stage("解決", 4.4, 7.2),
            Stage("実演", 7.2, 10.4),
            Stage("CTA", 10.4, 12.7),
        ]

    def test_full_contiguous_coverage(self):
        validate_stages(self.stages, 12.7)

    def test_rejects_gap(self):
        broken = list(self.stages)
        broken[1] = Stage("課題", 2.1, 4.4)
        with self.assertRaises(ValueError):
            validate_stages(broken, 12.7)

    def test_filter_keeps_top_safe_area_and_is_visual_only(self):
        f = ffmpeg_overlay_filters(self.stages, 12.7, "/tmp/font.ttc")
        self.assertIn("y=92", f)
        self.assertNotIn("audio", f.lower())

    def test_manual_posting_policy(self):
        p = posting_policy()
        self.assertTrue(p["zero_cost"])
        self.assertTrue(p["human_approval_required"])
        self.assertFalse(p["auto_post"])


if __name__ == "__main__":
    unittest.main()
