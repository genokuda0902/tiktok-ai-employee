import json
import tempfile
import unittest
from pathlib import Path
from readable_takeaway import GENRES, POLICY, CAPTION_START, Y, H, check_manifest, make_overlay

class TakeawayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.src = Path(self.tmp.name)/'source.mp4'
        self.src.write_bytes(b'test source')
        from readable_takeaway import sha256
        self.data = {'policy': POLICY, 'genre': 'ai', 'source_sha256': sha256(self.src),
                     'takeaway': 'まずは1つ選んで試す', 'start': 3.0, 'end': 5.7}
    def tearDown(self): self.tmp.cleanup()
    def test_ten_genres(self):
        for g in GENRES:
            self.data['genre']=g
            self.assertEqual(check_manifest(self.data,self.src,23)[0], 'まずは1つ選んで試す')
    def test_fail_closed_sha(self):
        self.data['source_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'SHA256'):check_manifest(self.data,self.src,23)
    def test_policy(self):
        self.data['policy']='PUBLISH'
        with self.assertRaises(ValueError):check_manifest(self.data,self.src,23)
    def test_genre(self):
        self.data['genre']='unknown'
        with self.assertRaises(ValueError):check_manifest(self.data,self.src,23)
    def test_bad_text(self):
        for s in ('','abc\npassword','長'*30):
            self.data['takeaway']=s
            with self.assertRaises(ValueError):check_manifest(self.data,self.src,23)
    def test_bad_interval(self):
        self.data['end']=25
        with self.assertRaises(ValueError):check_manifest(self.data,self.src,23)
    def test_safe_roi(self): self.assertLess(Y+H,CAPTION_START)
    def test_image_alpha_and_size(self):
        from PIL import Image
        p=Path(self.tmp.name)/'overlay.png'
        make_overlay('まずは1つ選んで試す','ai',p)
        im=Image.open(p)
        self.assertEqual(im.size,(850,132))
        self.assertEqual(im.mode,'RGBA')
        self.assertEqual(im.getpixel((0,0))[3],0)
        self.assertGreater(im.getpixel((100,60))[3],200)
    def test_overflow_rejected(self):
        with self.assertRaises(ValueError):make_overlay('あ'*17,'ai',Path(self.tmp.name)/'long.png')

if __name__=='__main__':unittest.main()
