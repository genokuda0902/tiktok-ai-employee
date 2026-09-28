import unittest

from video_engine.scene_asset_manifest import SceneAsset, validate_manifest, REQUIRED_BEATS


class SceneAssetManifestTests(unittest.TestCase):
    def good_assets(self):
        return [SceneAsset(beat, f"assets/{i}_{beat}.jpg", "owned", True)
                for i, beat in enumerate(REQUIRED_BEATS)]

    def test_six_distinct_approved_assets_pass(self):
        c = validate_manifest(self.good_assets())
        self.assertEqual(c["distinct_images"], 6)
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])

    def test_duplicate_image_fails_closed(self):
        assets = self.good_assets()
        assets[1] = SceneAsset("problem", assets[0].image_path, "owned", True)
        with self.assertRaisesRegex(ValueError, "distinct image"):
            validate_manifest(assets)

    def test_unapproved_or_uncleared_asset_fails_closed(self):
        assets = self.good_assets()
        assets[2] = SceneAsset("solution", "assets/new.jpg", "unknown", False)
        with self.assertRaisesRegex(ValueError, "not approved"):
            validate_manifest(assets)

    def test_wrong_beat_order_fails_closed(self):
        assets = self.good_assets()
        assets[0], assets[1] = assets[1], assets[0]
        with self.assertRaisesRegex(ValueError, "order"):
            validate_manifest(assets)


if __name__ == "__main__":
    unittest.main()
