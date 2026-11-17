import unittest
from pathlib import Path
from quality.cycle1513_audio_gate import check_audio
class TestAudioGate(unittest.TestCase):
 def test_missing_media(self):
  with self.assertRaises(FileNotFoundError): check_audio(Path('/not_found.mp4'))
