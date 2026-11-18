import unittest
from unittest.mock import patch
import json
from experiments.cycle1552.quality_gate import inspect

class GateTest(unittest.TestCase):
    @patch("experiments.cycle1552.quality_gate.subprocess.run")
    def test_silent_video_is_not_approved(self, run):
        run.return_value.stdout = json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920,"codec_name":"h264"}],"format":{"duration":"12"}})
        result = inspect("sample.mp4")
        self.assertTrue(result["checks"]["portrait_1080x1920"])
        self.assertFalse(result["checks"]["audio_track_present"])
        self.assertFalse(result["publication_approved"])

    @patch("experiments.cycle1552.quality_gate.subprocess.run")
    def test_audio_presence_does_not_prove_japanese_speech(self, run):
        run.return_value.stdout = json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920,"codec_name":"h264"},{"codec_type":"audio","codec_name":"aac"}],"format":{"duration":"12"}})
        result = inspect("sample.mp4")
        self.assertTrue(result["checks"]["audio_track_present"])
        self.assertFalse(result["checks"]["japanese_narration_verified"])
        self.assertFalse(result["publication_approved"])

if __name__ == "__main__":
    unittest.main()
