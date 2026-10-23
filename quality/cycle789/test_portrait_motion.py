import json
import sys
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from portrait_motion import validate,smoothstep,fade,crop_zoom,edge_blend
C=json.loads((Path(__file__).resolve().parent/'config.json').read_text(encoding='utf-8'))
class MotionTests(unittest.TestCase):
    def test_valid_contract(self): self.assertTrue(validate(C))
    def test_fail_closed(self):
        for field,value in [('mode','publish'),('rights_reviewed',True),('publication_approved',True)]:
            with self.assertRaises(ValueError): validate({**C,field:value})
    def test_safe_region(self):
        x=json.loads(json.dumps(C));x['regions'][0]['box']=[0,0,1080,1920]
        with self.assertRaises(ValueError):validate(x)
    def test_safe_zoom(self):
        x=json.loads(json.dumps(C));x['regions'][0]['zoom_to']=1.5
        with self.assertRaises(ValueError):validate(x)
    def test_timing(self):
        x=json.loads(json.dumps(C));x['regions'][0]['end']=x['regions'][0]['start']
        with self.assertRaises(ValueError):validate(x)
    def test_fade_ends_zero(self):
        self.assertEqual(fade(3.15,3.15,5.35),0.)
        self.assertEqual(fade(5.35,3.15,5.35),0.)
        self.assertGreater(fade(4.,3.15,5.35),.99)
    def test_ease_bounded(self):
        self.assertEqual(smoothstep(-2),0.)
        self.assertEqual(smoothstep(2),1.)
    def test_image_size_and_change(self):
        im=Image.new('RGB',(150,200),'black')
        for x in range(150):
            for y in range(200):im.putpixel((x,y),(x,y,0))
        z=crop_zoom(im,1.06)
        self.assertEqual(z.size,im.size)
        self.assertNotEqual(z.getpixel((0,0)),im.getpixel((0,0)))
    def test_cross_genre(self):
        for g in ['technology','business','career','finance','history','travel','food','health','lifestyle','science']:
            self.assertTrue(validate({**C,'genre':g}))
    def test_feather_no_seam(self):
        self.assertEqual(edge_blend(0),0.)
        self.assertEqual(edge_blend(22),1.)
        self.assertGreater(edge_blend(11),.49)
    def test_8pct_cap(self):
        with self.assertRaises(ValueError):crop_zoom(Image.new('RGB',(100,100)),1.2)
if __name__=='__main__':unittest.main()
