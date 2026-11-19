import unittest
from unittest.mock import patch
from audio_tail_fade import render
class TestFade(unittest.TestCase):
    @patch('audio_tail_fade.subprocess.check_output',return_value=b'{"format":{"duration":"22.75"}}')
    def test_invalid_input(self, probe):
        with self.assertRaises(ValueError): render('input.mp4','out.mp4',999)
