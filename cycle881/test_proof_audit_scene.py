import unittest
from dataclasses import replace
from pathlib import Path
import tempfile
from proof_audit_scene import (DEFAULT,GENRES,POLICY,CAPTIONS,START,END,TOP_HEIGHT,
    validate_proof,validate_manifest,progress,review_caption_alignment,sha256)

class TestProofAudit(unittest.TestCase):
    def test_all_ten_genres(self):
        for genre in GENRES:
            self.assertEqual(validate_proof(replace(DEFAULT,genre=genre)),(46,29))
    def test_mismatched_claim_rejected(self):
        with self.assertRaises(ValueError):validate_proof(replace(DEFAULT,expected=(47,29)))
    def test_negative_data_rejected(self):
        with self.assertRaises(ValueError):validate_proof(replace(DEFAULT,data=((12,8),(-1,9),(18,12))))
    def test_contact_rejected(self):
        with self.assertRaises(ValueError):validate_proof(replace(DEFAULT,footer='@account'))
    def test_url_rejected(self):
        with self.assertRaises(ValueError):validate_proof(replace(DEFAULT,title='https://example.com'))
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):validate_proof(replace(DEFAULT,genre='other'))
    def test_scene_boundaries(self):
        self.assertEqual((START,END,TOP_HEIGHT),(336,422,1450))
        self.assertEqual([progress(n) for n in (0,27,28,55,56,85)],[0,0,1,1,2,2])
        with self.assertRaises(ValueError):progress(86)
    def test_manifest_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'x.mp4';f.write_bytes(b'synthetic')
            with self.assertRaises(ValueError):validate_manifest(f,POLICY)
            self.assertTrue(validate_manifest(f,{**POLICY,'source_sha256':sha256(f)}))
    def test_voice_unverified_by_default(self):
        self.assertFalse(review_caption_alignment(CAPTIONS)['semantic_match_verified'])
    def test_voice_not_approved(self):
        self.assertFalse(review_caption_alignment(CAPTIONS,CAPTIONS)['semantic_match_verified'])
    def test_voice_text_mismatch(self):
        bad=list(CAPTIONS);bad[0]=('別の発話',.27,2.93)
        self.assertEqual(review_caption_alignment(CAPTIONS,bad,True)['status'],'MISMATCH')
    def test_voice_time_mismatch(self):
        bad=list(CAPTIONS);bad[0]=(bad[0][0],1.0,2.93)
        self.assertEqual(review_caption_alignment(CAPTIONS,bad,True)['status'],'MISMATCH')
    def test_manual_text_review_is_not_pronunciation_proof(self):
        r=review_caption_alignment(CAPTIONS,CAPTIONS,True)
        self.assertTrue(r['semantic_match_verified'])
        self.assertFalse(r['pronunciation_verified'])

if __name__=='__main__':unittest.main()
