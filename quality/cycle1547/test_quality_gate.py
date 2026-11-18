import unittest
from unittest.mock import patch
from quality.cycle1547.quality_gate import inspect

class GateTests(unittest.TestCase):
    @patch("quality.cycle1547.quality_gate.subprocess.run")
    def test_silent_or_effects_not_narration(self, run):
        run.return_value.stdout='{"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}],"format":{}}'
        result=inspect("synthetic.mp4")
        self.assertFalse(result["publication_allowed"])
        self.assertFalse(result["japanese_narration_verified"])
    @patch("quality.cycle1547.quality_gate.subprocess.run")
    def test_requires_every_approval(self, run):
        run.return_value.stdout='{"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}],"format":{}}'
        self.assertFalse(inspect("synthetic.mp4",True,True,True,False)["publication_allowed"])
        self.assertTrue(inspect("synthetic.mp4",True,True,True,True)["publication_allowed"])
if __name__=="__main__": unittest.main()
