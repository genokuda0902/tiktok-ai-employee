import unittest
from video_engine.quality.safe_hook import GENRES, SAFE, layout_bounds, render_frame, validate

class HookTest(unittest.TestCase):
    def setUp(self):
        self.m={'publication':'NOT_APPROVED','posting':'MANUAL_ONLY','asset_rights':'UNVERIFIED_REVIEW_ONLY','genre':GENRES[0],'baseline_sha256':'a'*64,'narration_status':'ABSENT','voice_caption_sync_verified':False,'numbers':[120,150,200,180],'duration_seconds':20}
    def test_ten_genres(self):
        self.assertEqual(len(set(GENRES)),10)
        for g in GENRES:self.assertTrue(validate({**self.m,'genre':g}))
    def test_reject_approval_claim(self):
        for key,val in [('publication','APPROVED'),('posting','AUTO'),('asset_rights','APPROVED'),('narration_status','VERIFIED_WAV'),('voice_caption_sync_verified',True),('numbers',[120,150,200,250])]:
            with self.subTest(key=key),self.assertRaises(ValueError):validate({**self.m,key:val})
    def test_safe_zone(self):
        for name,(top,bottom) in layout_bounds().items():
            with self.subTest(name=name):self.assertGreaterEqual(top,SAFE[0]);self.assertLessEqual(bottom,SAFE[1])
    def test_frame(self):
        im=render_frame(0);self.assertEqual(im.size,(1080,1920));self.assertNotEqual(im.getpixel((100,250)),im.getpixel((500,1800)))

if __name__=='__main__':unittest.main()
