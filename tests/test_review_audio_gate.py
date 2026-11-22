import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory
from src.review_audio_gate import inspect

class TestReviewAudioGate(unittest.TestCase):
    def test_missing_video_fails_closed(self):
        self.assertEqual(inspect('/nonexistent/review.mp4')['issues'], ['missing_mp4'])
    def test_video_without_audio_is_rejected(self):
        with TemporaryDirectory() as td:
            p=Path(td)/'a.mp4'; p.write_bytes(b'not-empty')
            fake={'streams':[{'codec_type':'video','width':1080,'height':1920}], 'format':{'duration':'20'}}
            from subprocess import CompletedProcess
            with patch('src.review_audio_gate.subprocess.run',return_value=CompletedProcess([],0,__import__('json').dumps(fake),'')):
                result=inspect(p)
            self.assertFalse(result['approved'])
            self.assertIn('narration_audio_missing',result['issues'])
            self.assertIn('speech_caption_sync_unverified',result['issues'])
    def test_audio_stream_does_not_prove_japanese(self):
        with TemporaryDirectory() as td:
            p=Path(td)/'a.mp4';p.write_bytes(b'x')
            fake={'streams':[{'codec_type':'video','width':1080,'height':1920},{'codec_type':'audio'}], 'format':{'duration':'20'}}
            from subprocess import CompletedProcess
            with patch('src.review_audio_gate.subprocess.run',return_value=CompletedProcess([],0,__import__('json').dumps(fake),'')):
                result=inspect(p)
            self.assertIn('japanese_speech_unverified',result['issues'])
