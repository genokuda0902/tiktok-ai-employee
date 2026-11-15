import unittest
from unittest.mock import patch
from pathlib import Path
from voice_highpass import process

class TestVoiceHighpass(unittest.TestCase):
    def test_invalid_cutoff(self):
        with self.assertRaises(ValueError): process("missing.mp4", "out.mp4", 200)
    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError): process("missing.mp4", "out.mp4")
    def test_command_preserves_video(self):
        with patch.object(Path, "is_file", return_value=True), patch("subprocess.run") as run:
            process("in.mp4", "out.mp4")
            cmd = run.call_args.args[0]
            self.assertEqual(cmd[cmd.index("-c:v")+1], "copy")
            self.assertIn("highpass=f=75", cmd)
if __name__ == "__main__": unittest.main()
