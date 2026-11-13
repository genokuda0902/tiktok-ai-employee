import unittest
from unittest.mock import patch
from qa_gate import validate
class TestGate(unittest.TestCase):
    @patch("qa_gate.probe")
    def test_tone_only_is_not_publication_ready(self,probe):
        probe.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertFalse(validate("review.mp4")["publication_approved"])
    @patch("qa_gate.probe")
    def test_low_resolution_rejected(self,probe):
        probe.return_value={"streams":[{"codec_type":"video","width":512,"height":910},{"codec_type":"audio"}]}
        self.assertFalse(validate("review.mp4",True,True)["technical_pass"])
if __name__=="__main__": unittest.main()
