import unittest
from unittest.mock import patch
import json
from quality_cycle1622 import inspect

class GateTests(unittest.TestCase):
    def probe(self, audio):
        streams = [{"codec_type":"video","width":720,"height":1280}]
        if audio: streams.append({"codec_type":"audio","codec_name":"aac"})
        return json.dumps({"streams":streams,"format":{"duration":"3"}}).encode()
    def test_silent_fails_closed(self):
        with patch("subprocess.check_output", return_value=self.probe(False)):
            self.assertFalse(inspect("demo.mp4",[{"start":0,"end":3,"text":"字幕"}],assets_approved=True,employee_approved=True)["posting_allowed"])
    def test_missing_approval_fails(self):
        with patch("subprocess.check_output", return_value=self.probe(True)):
            self.assertFalse(inspect("demo.mp4",[{"start":0,"end":3,"text":"字幕"}])["posting_allowed"])
    def test_full_approval(self):
        with patch("subprocess.check_output", return_value=self.probe(True)):
            self.assertTrue(inspect("demo.mp4",[{"start":0,"end":3,"text":"字幕"}],assets_approved=True,employee_approved=True)["posting_allowed"])

if __name__ == "__main__": unittest.main()
