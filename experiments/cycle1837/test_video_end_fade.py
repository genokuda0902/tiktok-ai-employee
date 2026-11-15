import unittest
from unittest.mock import patch
from video_end_fade import render

class FadeTests(unittest.TestCase):
    def test_preserves_audio(self):
        with patch('subprocess.run') as run:
            render('a.mp4','b.mp4',22.87)
            cmd=run.call_args.args[0]
            self.assertEqual(cmd[cmd.index('-c:a')+1],'copy')
    def test_rejects_bad_duration(self):
        with self.assertRaises(ValueError):
            render('a.mp4','b.mp4',0.2)
