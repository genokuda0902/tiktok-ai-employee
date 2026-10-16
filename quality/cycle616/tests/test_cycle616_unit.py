"""No external media or network required: validate cycle616 layout policy."""
import importlib.util, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('layout',ROOT/'layout.py')
layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout)
class LayoutTest(unittest.TestCase):
    def test_safe_bottom_for_organic_working_assumption(self):
        self.assertLess(layout.DEST[1]+layout.CROP[3]-layout.CROP[1],layout.SAFE_BOTTOM)
    def test_action_rail(self):
        self.assertLess(layout.DEST[0]+layout.CROP[2]-layout.CROP[0],900)
    def test_yuv420_even_crop(self):
        self.assertEqual((layout.CROP[2]-layout.CROP[0])%2,0)
        self.assertEqual((layout.CROP[3]-layout.CROP[1])%2,0)
    def test_plate_and_mask(self):
        import tempfile
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)
            layout.make_plate(p/'bg.png')
            layout.make_mask(p/'mask.png')
            self.assertEqual(Image.open(p/'bg.png').size,(1080,670))
            self.assertEqual(Image.open(p/'mask.png').size,(824,214))
if __name__=='__main__':unittest.main()
