import json, tempfile, unittest
from pathlib import Path
from reading_focus import GENRES,POLICY,X,Y,W,H,ROWS,sha256,validate,stage,overlay_frame

class ReadingFocusTest(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.src=Path(self.t.name)/'src';self.src.write_bytes(b'synthetic local only')
        self.m={'policy':POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,
                'source_sha256':sha256(self.src),'genre':'ai','layout_id':'writer_three_rows_v1','window':[1,3.5]}
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES:
            self.m['genre']=g;self.assertEqual(validate(self.m,self.src,5),(1,3.5))
            self.assertGreater(overlay_frame(g,37,75).getbbox()[2],0)
    def test_fail_closed(self):
        for k,val in [('policy','APPROVED'),('asset_approval','approved'),('manual_post_only',False),('source_sha256','bad'),('genre','bad'),('layout_id','other')]:
            x=dict(self.m);x[k]=val
            with self.assertRaises(ValueError):validate(x,self.src,5)
    def test_invalid_window(self):
        for w in [[-1,1.5],[1,2],[1,4],[4,6],['1',3.5],[1,1]]:
            x=dict(self.m);x['window']=w
            with self.assertRaises(ValueError):validate(x,self.src,5)
    def test_three_stages(self):
        self.assertEqual([stage(i,75) for i in [0,24,25,49,50,74]],[0,0,1,1,2,2])
    def test_subtitle_safe(self):
        self.assertLess(Y+H,1100)
        self.assertLess(X+W,950)
        self.assertTrue(all(x>=0 and y>=0 and x+w<=W and y+h<=H for x,y,w,h in ROWS))
    def test_transparent_and_fade(self):
        f0=overlay_frame('ai',0,75);fm=overlay_frame('ai',35,75)
        self.assertEqual(f0.size,(W,H))
        self.assertEqual(f0.getpixel((100,30))[3],0)
        self.assertLess(f0.getchannel('A').getextrema()[1],fm.getchannel('A').getextrema()[1])

if __name__=='__main__':unittest.main()
