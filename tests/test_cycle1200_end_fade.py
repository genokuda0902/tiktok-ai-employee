import unittest
from tools.cycle1200_end_fade import fade_start, command


class EndFadeTests(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(fade_start(23.033, 0.45), 22.583)

    def test_reject_bad_duration(self):
        with self.assertRaises(ValueError):
            fade_start(0)

    def test_reject_overlong_fade(self):
        with self.assertRaises(ValueError):
            fade_start(0.2, 0.45)

    def test_no_source_overwrite(self):
        with self.assertRaises(ValueError):
            command("same.mp4", "same.mp4", 23.033)

    def test_video_and_audio_both_fade(self):
        cmd = command("in.mp4", "out.mp4", 23.033)
        self.assertIn("-vf", cmd)
        self.assertIn("-af", cmd)


if __name__ == "__main__":
    unittest.main()
