import importlib.util
from pathlib import Path
import unittest

source = Path(__file__).resolve().parents[1] / "quality/cycle487/tts.py"
spec = importlib.util.spec_from_file_location("cycle487_tts", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class VoiceGateTests(unittest.TestCase):
    def test_six_japanese_scripts(self):
        self.assertEqual(len(module.SCRIPTS), 6)
        for sentence in module.SCRIPTS:
            self.assertTrue(any("\\u3040" <= c <= "\\u9fff" for c in sentence))

    def test_missing_binary_fails_closed(self):
        from unittest.mock import patch
        with patch("shutil.which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "unavailable"):
                module.synthesize("/tmp/voice_should_not_exist")

if __name__ == "__main__": unittest.main()
