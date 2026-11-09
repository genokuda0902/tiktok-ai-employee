import unittest
from unittest.mock import patch
import json
from quality.cycle1327_gate import inspect

class ReviewGateTests(unittest.TestCase):
    @patch('quality.cycle1327_gate.subprocess.run')
    def test_silent_rejected(self, run):
        run.return_value.stdout=json.dumps({'streams':[{'codec_type':'video','width':1080,'height':1920}]})
        self.assertIn('missing_japanese_narration_audio',inspect('demo.mp4')['errors'])
    @patch('quality.cycle1327_gate.subprocess.run')
    def test_audio_does_not_approve(self, run):
        run.return_value.stdout=json.dumps({'streams':[{'codec_type':'video','width':1080,'height':1920},{'codec_type':'audio'}]})
        self.assertFalse(inspect('demo.mp4')['publication_approved'])
