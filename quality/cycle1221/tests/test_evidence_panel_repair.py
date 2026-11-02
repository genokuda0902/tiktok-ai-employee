import importlib.util
import tempfile
import unittest
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('evidence_panel_repair',ROOT/'code/evidence_panel_repair.py')
mod=importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)

class PanelTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(mod.GENRES),10)
        for genre in mod.GENRES:
            mod.validate(mod.Patch(genre=genre))
    def test_reject_invalid_genre(self):
        with self.assertRaises(ValueError):mod.validate(mod.Patch(genre='secret'))
    def test_reject_subtitle_collision(self):
        with self.assertRaises(ValueError):mod.validate(mod.Patch(y=1170))
    def test_reject_missing_reviewed_text(self):
        with self.assertRaises(ValueError):mod.validate(mod.Patch(expression=''))
    def test_reject_oversized_expression(self):
        with self.assertRaises(ValueError):mod.validate(mod.Patch(expression='1'*43))
    def test_reject_out_of_bounds(self):
        with self.assertRaises(ValueError):mod.validate(mod.Patch(x=600))
    def test_overlay_transparency_and_roi(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'panel.png';mod.make_overlay(mod.Patch(),p)
            im=Image.open(p)
            self.assertEqual(im.size,(1080,1920))
            self.assertEqual(im.getpixel((200,1400))[3],0)
            self.assertEqual(im.getpixel((90,1090))[3],255)
    def test_text_must_fit(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                mod.make_overlay(mod.Patch(expression='W'*42),Path(d)/'panel.png')

if __name__=='__main__':unittest.main()
