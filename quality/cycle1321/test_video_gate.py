import unittest
from unittest.mock import patch
from quality.cycle1321.video_gate import validate

class VideoGateTests(unittest.TestCase):
    @patch('quality.cycle1321.video_gate.subprocess.run')
    @patch('quality.cycle1321.video_gate.probe')
    def test_silent_review_is_not_approved(self, probe, run):
        probe.return_value={'streams':[{'codec_type':'video','width':720,'height':1280}], 'format':{'duration':'12'}}
        result=validate('sample.mp4')
        self.assertFalse(result['audio_present'])
        self.assertFalse(result['publication_approved'])

    @patch('quality.cycle1321.video_gate.probe')
    def test_low_resolution_rejected(self, probe):
        probe.return_value={'streams':[{'codec_type':'video','width':512,'height':910}], 'format':{'duration':'12'}}
        with self.assertRaises(ValueError): validate('sample.mp4')

if __name__=='__main__': unittest.main()
