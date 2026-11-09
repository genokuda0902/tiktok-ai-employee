import unittest
from unittest.mock import patch
import json
from quality.cycle1328.qa_gate import inspect
class Tests(unittest.TestCase):
    @patch("subprocess.run")
    def test_silent_rejected(self,run):
        run.return_value.stdout=json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"12"}})
        self.assertIn("missing_narration_audio",inspect("demo.mp4")["issues"])
    @patch("subprocess.run")
    def test_audio_and_resolution_accepted(self,run):
        run.return_value.stdout=json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"12"}})
        self.assertTrue(inspect("demo.mp4")["approved"])
if __name__=="__main__":unittest.main()
