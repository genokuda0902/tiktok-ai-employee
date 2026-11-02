import tempfile,unittest
from pathlib import Path
from proof_first_hook import GENRES,POLICY,ROI,CAPTION_START,check,make_overlay,sha256

class ProofFirstTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.source=Path(self.tmp.name)/'source.bin';self.source.write_bytes(b'fake review media')
        self.manifest={'policy':POLICY,'genre':'ai','source_sha256':sha256(self.source),
            'asset_approval':'review_only_no_publication','manual_post_only':True,
            'proof_text':'46 ＋ 29 ＝ 75','proof_numbers':[46,29,75],
            'window':[0.12,1.5]}
    def test_all_ten_genres(self):
        for genre in GENRES:
            self.manifest['genre']=genre
            self.assertEqual(check(self.manifest,self.source,23.033),(0.12,1.5))
            p=Path(self.tmp.name)/(genre+'.png')
            self.assertTrue(make_overlay(self.manifest,p).exists())
    def test_source_pin(self):
        self.manifest['source_sha256']='x'
        with self.assertRaises(ValueError):check(self.manifest,self.source,23.033)
    def test_policy(self):
        self.manifest['policy']='PUBLISHED'
        with self.assertRaises(ValueError):check(self.manifest,self.source,23.033)
    def test_asset_approval(self):
        self.manifest.pop('asset_approval')
        with self.assertRaises(ValueError):check(self.manifest,self.source,23.033)
    def test_manual_only(self):
        self.manifest['manual_post_only']=False
        with self.assertRaises(ValueError):check(self.manifest,self.source,23.033)
    def test_numbers(self):
        self.manifest['proof_numbers']=[46,29,76]
        with self.assertRaises(ValueError):check(self.manifest,self.source,23.033)
    def test_unsafe_window(self):
        self.manifest['window']=[0.12,3.0]
        with self.assertRaises(ValueError):check(self.manifest,self.source,23.033)
    def test_long_text(self):
        self.manifest['proof_text']='あ'*31
        with self.assertRaises(ValueError):check(self.manifest,self.source,23.033)
    def test_caption_region(self):
        self.assertLess(ROI[1]+ROI[3],CAPTION_START)
    def test_no_newlines(self):
        self.manifest['proof_text']='bad\ntext'
        with self.assertRaises(ValueError):check(self.manifest,self.source,23.033)
if __name__=='__main__':unittest.main()
