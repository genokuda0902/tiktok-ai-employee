import unittest

from video_engine.image_slide_finishing import finishing_contract, finishing_filter


class ImageSlideFinishingTests(unittest.TestCase):
    def test_filter_is_zero_cost_ffmpeg_chain(self):
        chain = finishing_filter()
        self.assertIn("deband=", chain)
        self.assertIn("unsharp=", chain)

    def test_rejects_non_portrait_delivery(self):
        with self.assertRaises(ValueError):
            finishing_filter(720, 1280)

    def test_release_safety_is_preserved(self):
        contract = finishing_contract()
        self.assertTrue(contract["zero_cost"])
        self.assertTrue(contract["human_approval_required"])
        self.assertFalse(contract["auto_post"])
        self.assertFalse(contract["changes_audio"])
        self.assertFalse(contract["changes_caption_copy"])


if __name__ == "__main__":
    unittest.main()
