import unittest
from unittest.mock import patch
from quality.cycle1461.review_gate import inspect

class ReviewGateTest(unittest.TestCase):
    @patch('quality.cycle1461.review_gate.subprocess.check_output')
    def test_audio_does_not_imply_narration(self,probe):
        probe.return_value='{"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}]}'
        result=inspect('sample.mp4')
        self.assertTrue(result['audio_present'])
        self.assertFalse(result['japanese_narration_verified'])
        self.assertFalse(result['posting_allowed'])

if __name__=='__main__': unittest.main()
