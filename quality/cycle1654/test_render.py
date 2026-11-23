from pathlib import Path
import unittest

SCRIPT = Path(__file__).with_name("render.sh").read_text(encoding="utf-8")

class TimelineSafetyTest(unittest.TestCase):
    def test_no_automatic_publication(self):
        self.assertNotIn("tiktok upload", SCRIPT.lower())
    def test_four_steps(self):
        for n in range(1, 5):
            self.assertIn(f"STEP {n} / 4", SCRIPT)
    def test_requires_input_and_output(self):
        self.assertIn("input mp4 required", SCRIPT)
        self.assertIn("output mp4 required", SCRIPT)
    def test_silent_video_is_not_claimed_as_narrated(self):
        self.assertIn(" -an ", SCRIPT)

if __name__ == "__main__":
    unittest.main()
