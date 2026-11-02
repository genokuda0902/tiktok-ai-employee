import importlib.util
import tempfile
import unittest
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("review_disclosure",ROOT/"review_disclosure.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class DisclosureTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRES),10)
        self.assertEqual(len(set(m.GENRES)),10)
    def test_safe_area(self):
        self.assertLess(m.PANEL[3],m.CAPTION_START)
    def test_aaa_contrast(self):
        self.assertGreaterEqual(m.contrast(m.FG,m.BG),7)
    def test_approval_not_granted(self):
        self.assertIn("NOT_APPROVED",m.POLICY)
        self.assertIn("手動投稿",m.TEXT)
    def test_overlay_is_transparent_outside_panel(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"overlay.png"
            m.make_overlay(path)
            im=Image.open(path)
            self.assertEqual(im.size,(1080,1920))
            self.assertEqual(im.getpixel((200,1530))[3],0)
            self.assertEqual(im.getpixel((300,1350))[3],255)
    def test_hash(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"a.bin"
            p.write_bytes(b"original")
            self.assertEqual(m.sha(p),m.sha(p))

if __name__=="__main__":
    unittest.main()
