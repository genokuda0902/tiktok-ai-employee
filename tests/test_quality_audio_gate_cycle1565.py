import unittest
from unittest.mock import patch
from types import SimpleNamespace
from src.quality_audio_gate import check_audio
class Tests(unittest.TestCase):
 @patch("src.quality_audio_gate.subprocess.run")
 def test_silence(self,run):
  run.return_value=SimpleNamespace(returncode=0,stderr="mean_volume: -91.0 dB")
  self.assertFalse(check_audio("x")["approved"])
 @patch("src.quality_audio_gate.subprocess.run")
 def test_effects_not_speech(self,run):
  run.return_value=SimpleNamespace(returncode=0,stderr="mean_volume: -12.0 dB")
  self.assertIn("japanese_narration_unverified",check_audio("x")["blockers"])
 @patch("src.quality_audio_gate.subprocess.run")
 def test_verified(self,run):
  run.return_value=SimpleNamespace(returncode=0,stderr="mean_volume: -18.0 dB")
  self.assertTrue(check_audio("x",True,True,True)["approved"])
