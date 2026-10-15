import importlib.util, unittest
from pathlib import Path
from PIL import Image
spec=importlib.util.spec_from_file_location('c',Path(__file__).with_name('cycle594_guided_cursor.py'))
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
class QualityTests(unittest.TestCase):
    def test_genres(self):
        for g in c.GENRES:
            with self.subTest(genre=g): self.assertTrue(c.validate(g))
    def test_rejects_wrong_total(self):
        with self.assertRaises(ValueError): c.validate(c.GENRES[0],(120,150,200,251))
    def test_rejects_invalid_type(self):
        with self.assertRaises(ValueError): c.validate(c.GENRES[0],(120,150,200,True))
    def test_rejects_unknown_genre(self):
        with self.assertRaises(ValueError): c.validate('unknown')
    def test_stage_boundaries(self):
        self.assertEqual([c.stage_at(t) for t in (0,.99,1,1.99,2,2.99)],[0,0,1,1,2,2])
        for t in (-.1,3):
            with self.assertRaises(ValueError): c.stage_at(t)
    def test_overlay_dimensions(self):
        for t in (.2,1.2,2.2):
            x=c.overlay(Image.new('RGBA',(c.W,c.H),'white'),t)
            self.assertEqual(x.size,(1080,1920))
if __name__=='__main__': unittest.main()
