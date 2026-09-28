import unittest

from video_engine.scene_asset_manifest import REQUIRED_BEATS, SceneAsset
from video_engine.semantic_render_plan import SemanticBeat, build_render_plan, release_policy


class SemanticRenderPlanTests(unittest.TestCase):
    def _beats(self):
        return [
            SemanticBeat(
                beat=beat,
                asset=SceneAsset(beat, f"assets/{i}-{beat}.png", "owned", True),
                narration=f"日本語ナレーション{i}",
                caption=f"字幕{i}",
                duration_s=2.0,
            )
            for i, beat in enumerate(REQUIRED_BEATS)
        ]

    def test_six_beats_share_one_timeline(self):
        plan = build_render_plan(self._beats())
        self.assertEqual(len(plan), 6)
        self.assertEqual(tuple(x["beat"] for x in plan), REQUIRED_BEATS)
        self.assertEqual(plan[-1]["end"], 12.0)

    def test_duplicate_image_fails_closed(self):
        beats = self._beats()
        beats[1] = SemanticBeat("problem", SceneAsset("problem", beats[0].asset.image_path, "owned", True), "日本語", "字幕", 2.0)
        with self.assertRaises(ValueError):
            build_render_plan(beats)

    def test_unapproved_asset_fails_closed(self):
        beats = self._beats()
        beats[2] = SemanticBeat("solution", SceneAsset("solution", "assets/x.png", "owned", False), "日本語", "字幕", 2.0)
        with self.assertRaises(ValueError):
            build_render_plan(beats)

    def test_release_is_manual_only(self):
        p = release_policy()
        self.assertEqual((p["width"], p["height"]), (1080, 1920))
        self.assertTrue(p["zero_cost"])
        self.assertTrue(p["human_approval_required"])
        self.assertTrue(p["manual_post_only"])
        self.assertFalse(p["auto_post"])


if __name__ == "__main__":
    unittest.main()
