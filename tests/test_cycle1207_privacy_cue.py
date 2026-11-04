import unittest
from pathlib import Path
from unittest.mock import patch
from tools.cycle1207_privacy_cue import video_filter, render

class PrivacyCueTests(unittest.TestCase):
    def test_window(self):
        self.assertIn("between(t,6,9)", video_filter())
    def test_no_bad_interval(self):
        with self.assertRaises(ValueError):
            video_filter(9, 6)
    def test_missing_source_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            render("/definitely/not/here.mp4", "/tmp/should-not-exist.mp4")
    def test_audio_is_copied(self):
        with patch("subprocess.run") as run, patch.object(Path, "is_file", return_value=True):
            render("input.mp4", "output.mp4")
            self.assertIn("-c:a", run.call_args.args[0])
            self.assertIn("copy", run.call_args.args[0])

if __name__ == "__main__":
    unittest.main()
