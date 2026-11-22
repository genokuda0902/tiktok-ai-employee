import unittest
from pathlib import Path

class ReviewGate(unittest.TestCase):
    def test_burned_captions_do_not_imply_speech(self):
        text = Path(__file__).with_name("render_burned_captions.sh").read_text()
        self.assertIn("-an", text)
        self.assertIn("subtitles=", text)
    def test_manual_approval_required(self):
        manifest = Path(__file__).with_name("cycle1651_manifest.json").read_text()
        self.assertIn('"posting_allowed": false', manifest)
        self.assertIn('"japanese_narration_verified": false', manifest)

if __name__ == "__main__":
    unittest.main()
