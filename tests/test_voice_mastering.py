import unittest
from video_engine.voice_mastering import build_command, build_filter


class VoiceMasteringTests(unittest.TestCase):
    def test_filter_has_speech_band_and_loudness_target(self):
        f = build_filter()
        self.assertIn("highpass=f=80", f)
        self.assertIn("lowpass=f=14500", f)
        self.assertIn("loudnorm=I=-16", f)
        self.assertIn("TP=-1.5", f)

    def test_video_is_stream_copied(self):
        cmd = build_command("in.mp4", "out.mp4")
        self.assertIn("copy", cmd)
        self.assertIn("192k", cmd)

    def test_non_mp4_fails_closed(self):
        with self.assertRaises(ValueError):
            build_command("in.mov", "out.mp4")


if __name__ == "__main__":
    unittest.main()
