"""Dependency-free CI subset. Full image/MP4 tests run locally with Pillow/FFmpeg."""
import sys
import types
import unittest

# Stub PIL solely for importing pure manifest/ASR functions; do not claim image QA.
if 'PIL' not in sys.modules:
    pil = types.ModuleType('PIL')
    pil.Image = object()
    pil.ImageDraw = object()
    pil.ImageFont = object()
    sys.modules['PIL'] = pil

from narrative_rail import GENRES, ACTS, act_for_time, normalize_ja, audit_transcript, validate_manifest, publication_gate

GOOD = {'genre':'ai_work','publication_approved':False,'employee_approval':False,
        'asset_rights_approved':False,'upload_media_to_github':False,
        'automatic_posting':False,'paid_service':False,
        'independent_japanese_asr_verified':False,'caption_semantics_verified':False,
        'source_sha256':'a'*64}

class OfflinePolicyTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES: self.assertTrue(validate_manifest({**GOOD,'genre':g}))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): validate_manifest({**GOOD,'genre':'other'})
    def test_all_release_flags_fail_closed(self):
        for k in ('publication_approved','employee_approval','asset_rights_approved',
                  'upload_media_to_github','automatic_posting','paid_service',
                  'independent_japanese_asr_verified','caption_semantics_verified'):
            with self.subTest(k=k),self.assertRaises(ValueError):
                validate_manifest({**GOOD,k:True})
    def test_missing_flag_fails(self):
        m=dict(GOOD); del m['paid_service']
        with self.assertRaises(ValueError):validate_manifest(m)
    def test_source_sha_fails(self):
        with self.assertRaises(ValueError):validate_manifest({**GOOD,'source_sha256':'bad'})
    def test_three_acts(self):
        self.assertEqual(ACTS,('課題','手順','確認'))
        self.assertEqual([act_for_time(t) for t in (0,5.667,17,23)],[0,1,2,2])
    def test_time_range(self):
        with self.assertRaises(ValueError):act_for_time(-1)
    def test_ja_normalization(self):
        self.assertEqual(normalize_ja('ＡＩ、仕事！'),normalize_ja('AI仕事'))
    def test_missing_asr_fails(self):
        self.assertFalse(audit_transcript([{'start':0,'end':1,'text':'確認'}],[])['passed'])
    def test_asr_similarity_and_time(self):
        a=[{'start':0,'end':1,'text':'数値を確認。'}]
        self.assertTrue(audit_transcript(a,[{'start':.1,'end':1.1,'text':'数値を確認'}])['passed'])
        self.assertFalse(audit_transcript(a,[{'start':2,'end':3,'text':'数値を確認'}])['passed'])
        self.assertFalse(audit_transcript(a,[{'start':0,'end':1,'text':'今日は晴天です'}])['passed'])
    def test_segment_count(self):
        self.assertFalse(audit_transcript([{'start':0,'end':1,'text':'確認'}],
                                          [{'start':0,'end':1,'text':'確認'},{'start':1,'end':2,'text':'次'}])['passed'])
    def test_no_publication(self):
        with self.assertRaises(PermissionError):publication_gate({})

if __name__=='__main__':unittest.main()
