import unittest
from unittest.mock import patch
import json
from quality.cycle1306.qa import inspect_video

class ReviewGateTests(unittest.TestCase):
    @patch("quality.cycle1306.qa.subprocess.run")
    def test_silent_is_not_approved(self, run):
        run.return_value.stdout=json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"15"}})
        result=inspect_video("sample.mp4", narration_verified=True, captions_verified=True, assets_approved=True, employee_approved=True)
        self.assertFalse(result["publish_allowed"])
        self.assertFalse(result["checks"]["japanese_narration_verified"])

    @patch("quality.cycle1306.qa.subprocess.run")
    def test_audio_alone_not_enough(self, run):
        run.return_value.stdout=json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"15"}})
        self.assertFalse(inspect_video("sample.mp4")["publish_allowed"])

if __name__ == "__main__":
    unittest.main()
