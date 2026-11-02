import json,tempfile,unittest
from pathlib import Path
from PIL import Image
from prompt_contrast import POLICY,GENRES,draw_overlay,validate,PANEL,sha256

class Tests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.d=Path(self.t.name);self.src=self.d/'source';self.src.write_bytes(b'fictional')
        self.m={'policy':POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,
                'source_sha256':sha256(self.src),'genre':'ai','window':[8.75,10.85]}
    def tearDown(self):self.t.cleanup()
    def test_genres(self):self.assertEqual(len(GENRES),10)
    def test_policy(self):self.assertEqual(validate(self.m,self.src,23), (8.75,10.85))
    def test_reject_publication(self):
        self.m['asset_approval']='approved';self.assertRaises(ValueError,validate,self.m,self.src,23)
    def test_reject_manual_post_false(self):
        self.m['manual_post_only']=False;self.assertRaises(ValueError,validate,self.m,self.src,23)
    def test_reject_unpinned(self):
        self.m['source_sha256']='bad';self.assertRaises(ValueError,validate,self.m,self.src,23)
    def test_reject_unknown_genre(self):
        self.m['genre']='other';self.assertRaises(ValueError,validate,self.m,self.src,23)
    def test_reject_short(self):
        self.m['window']=[8.75,9.1];self.assertRaises(ValueError,validate,self.m,self.src,23)
    def test_reject_end(self):
        self.m['window']=[8.75,25.1];self.assertRaises(ValueError,validate,self.m,self.src,23)
    def test_transparent_subtitle_area(self):
        p=self.d/'ov.png';draw_overlay(self.m,p);im=Image.open(p)
        self.assertEqual(im.size,(1080,1920));self.assertEqual(im.getpixel((300,1400))[3],0)
        self.assertEqual(im.getpixel((300,1700))[3],0)
        self.assertGreater(im.getpixel((300,1160))[3],200)
    def test_content_nontransparent(self):
        p=self.d/'ov.png';draw_overlay(self.m,p);self.assertGreater(Image.open(p).getpixel((300,550))[3],200)
    def test_all_genres_overlay(self):
        for g in GENRES:
            self.m['genre']=g;draw_overlay(self.m,self.d/(g+'.png'))
            self.assertTrue((self.d/(g+'.png')).exists())

if __name__=='__main__':unittest.main()
