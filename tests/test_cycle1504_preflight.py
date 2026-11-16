import json
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from quality.cycle1504_preflight import inspect

class GateTests(unittest.TestCase):
    @patch("quality.cycle1504_preflight.subprocess.run")
    def test_aac_is_not_narration(self, run):
        run.return_value=SimpleNamespace(stdout=json.dumps({"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio","codec_name":"aac"}]}))
        result=inspect("demo.mp4")
        self.assertFalse(result["publication_approved"])
        self.assertIn("japanese_narration_unverified",result["issues"])
    @patch("quality.cycle1504_preflight.subprocess.run")
    def test_requires_explicit_checks(self, run):
        run.return_value=SimpleNamespace(stdout=json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}))
        self.assertTrue(inspect("demo.mp4",True,True,True)["publication_approved"])
if __name__=="__main__": unittest.main()
