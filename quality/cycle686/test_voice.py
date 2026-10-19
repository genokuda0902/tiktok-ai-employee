"""Offline TTS fail-closed and timing contracts, no network needed."""
import sys, unittest, tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from voice import GENRES, LINES, timestamp, build

class TestVoice(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(GENRES),10)
 def test_ten_scenes(self): self.assertEqual(len(LINES),10)
 def test_srt_timestamp(self): self.assertEqual(timestamp(2.135),'00:00:02,135')
 def test_reject_unknown_genre(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError): build(d,'unknown')
 def test_no_fake_audio(self):
  with tempfile.TemporaryDirectory() as d:
   from unittest.mock import patch
   with patch('voice.shutil.which',return_value=None):
    with self.assertRaisesRegex(RuntimeError,'no narration generated'): build(d)
   self.assertFalse((Path(d)/'narration_ja.wav').exists())

if __name__=='__main__': unittest.main()
