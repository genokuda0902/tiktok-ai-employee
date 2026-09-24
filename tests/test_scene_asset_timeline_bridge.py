import unittest

from video_engine.scene_asset_manifest import SceneAsset
from video_engine.scene_asset_timeline_bridge import SceneCopy, build_asset_timeline, delivery_policy


BEATS = ("hook", "problem", "solution", "demo", "result", "cta")


def assets():
    return [SceneAsset(b, f"approved/{i}_{b}.png", "owned", True) for i, b in enumerate(BEATS)]


def copy():
    return [SceneCopy(b, f"日本語ナレーション{i}", f"字幕{i}", 1.0 + i * 0.2) for i, b in enumerate(BEATS)]


class SceneAssetTimelineBridgeTests(unittest.TestCase):
    def test_builds_six_distinct_semantic_rows(self):
        rows = build_asset_timeline(assets(), copy())
        self.assertEqual([r["beat"] for r in rows], list(BEATS))
        self.assertEqual(len({r["image"] for r in rows}), 6)
        self.assertTrue(all(r["approved"] for r in rows))

    def test_rejects_duplicate_asset(self):
        a = assets()
        a[5] = SceneAsset("cta", a[0].image_path, "owned", True)
        with self.assertRaises(ValueError):
            build_asset_timeline(a, copy())

    def test_rejects_unapproved_asset(self):
        a = assets()
        a[2] = SceneAsset("solution", a[2].image_path, "owned", False)
        with self.assertRaises(ValueError):
            build_asset_timeline(a, copy())

    def test_rejects_copy_order_mismatch(self):
        c = copy()
        c[0], c[1] = c[1], c[0]
        with self.assertRaises(ValueError):
            build_asset_timeline(assets(), c)

    def test_manual_post_policy_is_fail_closed(self):
        p = delivery_policy()
        self.assertTrue(p["manual_post_only"])
        self.assertFalse(p["auto_post"])
        self.assertTrue(p["human_quality_review_required"])
        self.assertTrue(p["human_rights_review_required"])


if __name__ == "__main__":
    unittest.main()
