import unittest

from video_engine.native_vertical_card_contract import NativeVerticalCard, release_policy


class NativeVerticalCardTests(unittest.TestCase):
    def test_default_contract_passes(self):
        NativeVerticalCard().validate()

    def test_wrong_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            NativeVerticalCard(width=720, height=1280).validate()

    def test_dense_copy_fails_closed(self):
        with self.assertRaises(ValueError):
            NativeVerticalCard(max_title_chars=40).validate()

    def test_unsafe_margin_fails_closed(self):
        with self.assertRaises(ValueError):
            NativeVerticalCard(safe_left=20).validate()

    def test_release_remains_manual_and_zero_cost(self):
        p = release_policy()
        self.assertTrue(p["zero_cost"])
        self.assertTrue(p["image_first"])
        self.assertTrue(p["human_rights_approval_required"])
        self.assertTrue(p["human_quality_approval_required"])
        self.assertTrue(p["manual_post_only"])
        self.assertFalse(p["auto_post"])


if __name__ == "__main__":
    unittest.main()
