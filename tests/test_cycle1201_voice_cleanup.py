import unittest
from pathlib import Path
from tools.cycle1201_voice_cleanup import command, FILTER

class TestVoiceCleanup(unittest.TestCase):
    def test_video_stream_preserved(self):
        args = command(Path('input.mp4'), Path('out.mp4'))
        self.assertEqual(args[args.index('-c:v') + 1], 'copy')
    def test_audio_filter_and_encoding(self):
        args = command(Path('input.mp4'), Path('out.mp4'))
        self.assertIn('alimiter=limit=0.89', args[args.index('-af') + 1])
        self.assertIn('highpass=f=80', FILTER)
        self.assertEqual(args[args.index('-c:a') + 1], 'aac')
    def test_reject_same_path(self):
        with self.assertRaises(ValueError): command(Path('a.mp4'), Path('./a.mp4'))
    def test_reject_non_mp4(self):
        with self.assertRaises(ValueError): command(Path('a.mov'), Path('b.mp4'))
