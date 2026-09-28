import unittest

from video_engine.deband_finish import ffmpeg_filter, safety_contract


class DebandFinishTests(unittest.TestCase):
    def test_filter_is_deband_only(self):
        f = ffmpeg_filter()
        self.assertIn("deband=", f)
        self.assertNotIn("unsharp", f)

    def test_wrong_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(720, 1280)

    def test_release_policy_preserved(self):
        c = safety_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_audio"])
        self.assertTrue(c["preserve_caption_copy"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])
        self.assertFalse(c["second_sharpen"])


if __name__ == "__main__":
    unittest.main()
