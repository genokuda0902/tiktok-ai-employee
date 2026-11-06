import unittest
from unittest.mock import patch
from quality.cycle1251.check_media import validate

class MediaTests(unittest.TestCase):
    @patch("quality.cycle1251.check_media.subprocess.run")
    @patch("quality.cycle1251.check_media.probe")
    def test_missing_audio_fails_closed(self, probe, run):
        probe.return_value = {"streams": [{"codec_type": "video", "width": 720, "height": 1280}]}
        with self.assertRaisesRegex(ValueError, "audio track missing"):
            validate("test.mp4")
        run.assert_not_called()

    @patch("quality.cycle1251.check_media.subprocess.run")
    @patch("quality.cycle1251.check_media.probe")
    def test_audio_does_not_imply_narration(self, probe, run):
        probe.return_value = {"streams": [{"codec_type": "video", "width": 720, "height": 1280}, {"codec_type": "audio"}]}
        result = validate("test.mp4")
        self.assertEqual(result["japanese_narration"], "NOT_VERIFIED")
        self.assertFalse(result["publication_approved"])
