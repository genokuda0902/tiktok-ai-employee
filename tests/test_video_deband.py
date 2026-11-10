import pathlib
import unittest

SOURCE=pathlib.Path(__file__).resolve().parents[1]/"tools"/"video_deband.py"

class TestVideoDeband(unittest.TestCase):
    def test_common_ffmpeg_settings(self):
        code=SOURCE.read_text()
        for required in ("deband=", "libx264", "yuv420p", "+faststart", '"copy"'):
            self.assertIn(required,code)
    def test_safe_optional_module(self):
        import ast
        ast.parse(SOURCE.read_text())

if __name__=="__main__":
    unittest.main()
