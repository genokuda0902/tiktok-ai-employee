"""Cycle824 CI safety and visual regression tests."""
import importlib.util, pathlib, unittest
from PIL import Image, ImageChops
p=pathlib.Path(__file__).resolve().parent/'cycle824_ci.py'
spec=importlib.util.spec_from_file_location('cycle824_ci',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestCycle824(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.PALETTES),10)
    def test_laptop_spatial_change(self):
        base=Image.new('RGB',(1080,1920),'#FFFFFF')
        # Upgrade operates on original source without remote images.
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/'scene.png';base.save(p)
            m.upgrade_scene(p,1)
            upgraded=Image.open(p)
            self.assertEqual(upgraded.size,(1080,1920))
            self.assertNotEqual(upgraded.getpixel((550,1170)),(255,255,255))
    def test_no_publication(self):
        import inspect
        s=inspect.getsource(m)
        self.assertIn('review_only',s)
        self.assertNotIn('requests.post(',s)
if __name__=='__main__':unittest.main()
