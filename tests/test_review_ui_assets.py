import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from review_ui_assets import HEIGHT, WIDTH, make_sanitized_ui_frame


class ReviewUiAssetTests(unittest.TestCase):
    def test_generates_portrait_png_without_external_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            out = make_sanitized_ui_frame(Path(directory) / 'frame.png', 0)
            data = out.read_bytes()
            self.assertTrue(data.startswith(b'\x89PNG\r\n\x1a\n'))
            width, height = struct.unpack('>II', data[16:24])
            self.assertEqual((width, height), (WIDTH, HEIGHT))
            self.assertGreater(len(data), 1000)

    def test_variants_are_deterministic_and_visually_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a1 = make_sanitized_ui_frame(root / 'a1.png', 1).read_bytes()
            a2 = make_sanitized_ui_frame(root / 'a2.png', 1).read_bytes()
            b = make_sanitized_ui_frame(root / 'b.png', 2).read_bytes()
            self.assertEqual(a1, a2)
            self.assertNotEqual(a1, b)


if __name__ == '__main__':
    unittest.main()
