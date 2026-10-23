import copy,json,unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
from focus_guidance import validate,intersect,make_overlay,GENRES
C=json.loads((Path(__file__).parent/'config.json').read_text(encoding='utf-8'))
class TestFocus(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(C))
    def test_ten_genres(self):
        for g in GENRES:
            c=copy.deepcopy(C);c['genre']=g;self.assertTrue(validate(c))
    def test_unknown_genre(self):
        c=copy.deepcopy(C);c['genre']='unknown'
        with self.assertRaises(ValueError):validate(c)
    def test_publication_fail_closed(self):
        for k in ('rights_reviewed','publication_approved'):
            c=copy.deepcopy(C);c[k]=True
            with self.assertRaises(ValueError):validate(c)
    def test_unsafe_top(self):
        c=copy.deepcopy(C);c['focus_events'][0]['box'][1]=1
        with self.assertRaises(ValueError):validate(c)
    def test_unsafe_right(self):
        c=copy.deepcopy(C);c['focus_events'][1]['box'][0]=1000
        with self.assertRaises(ValueError):validate(c)
    def test_caption_collision(self):
        c=copy.deepcopy(C);c['protected_caption_box']=[120,1000,700,200]
        with self.assertRaises(ValueError):validate(c)
    def test_bad_timing(self):
        c=copy.deepcopy(C);c['focus_events'][1]['start']=7.0
        with self.assertRaises(ValueError):validate(c)
    def test_geometry(self):self.assertEqual(intersect([0,0,100,100],[200,200,30,30]),0)
    def test_overlay_alpha(self):
        with TemporaryDirectory() as td:
            p=Path(td)/'overlay.png';make_overlay(C['focus_events'][0]['box'],'input',p)
            im=Image.open(p)
            self.assertEqual(im.size,(1080,1920))
            self.assertEqual(im.getpixel((550,1100))[3],0)
            self.assertGreater(im.getpixel((128,1000))[3],0)
    def test_no_confidential_asset_paths(self):
        self.assertNotIn('IMG_5805',str(C));self.assertNotIn('v33_REAL',str(C))
if __name__=='__main__':unittest.main()
