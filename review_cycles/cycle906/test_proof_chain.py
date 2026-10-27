import tempfile
import unittest
from pathlib import Path
from proof_chain import (GENRES, START_FRAME, END_FRAME, OVERLAY_TOP, OVERLAY_HEIGHT,
                         CAPTION_START_Y, active_step, frame_image, make_frames,
                         validate_manifest, publication_gate, REVIEW_STATUS)

GOOD = {'genre':'ai_work','publication_approved':False,'employee_approval':False,
        'asset_rights_approved':False,'upload_media_to_github':False,
        'automatic_posting':False,'paid_service':False,'contains_private_data':False,
        'caption_semantics_verified':False,'independent_japanese_asr_verified':False,
        'source_sha256':'a'*64}

class ProofChainTest(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            validate_manifest({**GOOD, 'genre':genre})
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError): validate_manifest({**GOOD, 'genre':'other'})
    def test_no_publication_or_upload(self):
        for k in ('publication_approved','employee_approval','asset_rights_approved','upload_media_to_github','automatic_posting','paid_service'):
            with self.subTest(k=k), self.assertRaises(ValueError):
                validate_manifest({**GOOD,k:True})
    def test_no_private_data(self):
        with self.assertRaises(ValueError): validate_manifest({**GOOD,'contains_private_data':True})
    def test_no_fake_asr_claims(self):
        for k in ('independent_japanese_asr_verified','caption_semantics_verified'):
            with self.assertRaises(ValueError):validate_manifest({**GOOD,k:True})
    def test_sha_required(self):
        with self.assertRaises(ValueError):validate_manifest({**GOOD,'source_sha256':'abc'})
    def test_stage_progression(self):
        self.assertEqual([active_step(i) for i in (0,26,27,53,54,80)], [0,0,1,1,2,2])
    def test_out_of_range(self):
        for x in (-1,81):
            with self.assertRaises(ValueError):active_step(x)
    def test_frame_geometry(self):
        im=frame_image(40)
        self.assertEqual(im.size,(980,98));self.assertEqual(im.mode,'RGBA')
    def test_caption_safety(self):
        self.assertLess(OVERLAY_TOP+OVERLAY_HEIGHT,CAPTION_START_Y)
        self.assertEqual(END_FRAME-START_FRAME+1,81)
    def test_smoke_png(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(make_frames(td,3),3)
            self.assertEqual(len(list(Path(td).glob('frame_*.png'))),3)
    def test_reject_frame_count(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):make_frames(td,82)
    def test_release_fail_closed(self):
        with self.assertRaises(PermissionError):publication_gate({'status':REVIEW_STATUS})

if __name__ == '__main__':unittest.main()
