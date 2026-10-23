import json
import unittest
from pathlib import Path
from PIL import Image
from repair_wipe import validate,wipe_frame

CFG=json.loads((Path(__file__).parent/'config.json').read_text())
class WipeTest(unittest.TestCase):
    def test_valid_config(self):self.assertTrue(validate(CFG))
    def test_reject_publication(self):
        x=dict(CFG,publication_approved=True)
        with self.assertRaises(ValueError):validate(x)
    def test_reject_rights_claim(self):
        x=dict(CFG,rights_reviewed=True)
        with self.assertRaises(ValueError):validate(x)
    def test_reject_overlap(self):
        x=dict(CFG,fixes=[CFG['fixes'][0],dict(CFG['fixes'][0])])
        with self.assertRaises(ValueError):validate(x)
    def test_reject_long_transition(self):
        x=dict(CFG,fixes=[dict(CFG['fixes'][0],last_frame=450,after_at=15.2)])
        with self.assertRaises(ValueError):validate(x)
    def test_opaque_pixels_not_blended(self):
        a=Image.new('RGB',(1080,1920),(200,20,20))
        b=Image.new('RGB',(1080,1920),(10,30,220))
        out=wipe_frame(a,b,.5)
        self.assertEqual(out.getpixel((100,800)),(10,30,220))
        self.assertEqual(out.getpixel((980,800)),(200,20,20))
    def test_start_end_exact(self):
        a=Image.new('RGB',(1080,1920),'red');b=Image.new('RGB',(1080,1920),'blue')
        self.assertEqual(wipe_frame(a,b,0).getpixel((540,100)),(255,0,0))
        self.assertEqual(wipe_frame(a,b,1).getpixel((540,100)),(0,0,255))
if __name__=='__main__':unittest.main()
