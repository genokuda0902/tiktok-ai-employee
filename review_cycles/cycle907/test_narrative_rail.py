import tempfile
import unittest
from pathlib import Path
from narrative_rail import (ACTS, GENRES, RAIL_POS, RAIL_SIZE, CAPTION_START_Y,
                            STATUS, act_for_time, rail_image, validate_manifest,
                            normalize_ja, audit_transcript, publication_gate)
GOOD = {'genre': 'ai_work', 'publication_approved': False, 'employee_approval': False,
        'asset_rights_approved': False, 'upload_media_to_github': False,
        'automatic_posting': False, 'paid_service': False,
        'independent_japanese_asr_verified': False, 'caption_semantics_verified': False,
        'source_sha256': 'a'*64}

class RailTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for g in GENRES: self.assertTrue(validate_manifest({**GOOD, 'genre': g}))
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError): validate_manifest({**GOOD, 'genre': 'invalid'})
    def test_fail_closed_flags(self):
        for key in ('publication_approved', 'employee_approval', 'asset_rights_approved',
                    'upload_media_to_github', 'automatic_posting', 'paid_service',
                    'independent_japanese_asr_verified', 'caption_semantics_verified'):
            with self.subTest(key=key), self.assertRaises(ValueError): validate_manifest({**GOOD, key: True})
    def test_missing_manifest_flag_rejected(self):
        m = dict(GOOD); del m['paid_service']
        with self.assertRaises(ValueError): validate_manifest(m)
    def test_source_hash_required(self):
        with self.assertRaises(ValueError): validate_manifest({**GOOD, 'source_sha256': 'no'})
    def test_act_boundaries(self):
        self.assertEqual([act_for_time(t) for t in (0, 5.666, 5.667, 16.999, 17., 23.)], [0,0,1,1,2,2])
    def test_invalid_times(self):
        for t in (-1., 24.):
            with self.assertRaises(ValueError): act_for_time(t)
    def test_rail_image(self):
        self.assertEqual(rail_image(1).size, RAIL_SIZE)
        self.assertEqual(rail_image(1).mode, 'RGBA')
    def test_caption_safety(self):
        self.assertLess(RAIL_POS[1] + RAIL_SIZE[1], CAPTION_START_Y)
    def test_rail_png_smoke(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'rail.png'; rail_image(2).save(p); self.assertGreater(p.stat().st_size, 1000)
    def test_ja_normalization(self):
        self.assertEqual(normalize_ja('ＡＩ、仕事！'), normalize_ja('AI仕事'))
    def test_asr_missing_fails(self):
        self.assertFalse(audit_transcript([{'start':0,'end':1,'text':'確認'}], [])['passed'])
    def test_asr_semantics_pass(self):
        a = [{'start':0,'end':1,'text':'数値を確認。'}]
        b = [{'start':.1,'end':1.1,'text':'数値を確認'}]
        self.assertTrue(audit_transcript(a,b)['passed'])
    def test_asr_mismatch_fails(self):
        a = [{'start':0,'end':1,'text':'数値を確認'}]
        b = [{'start':0,'end':1,'text':'今日は晴天です'}]
        self.assertFalse(audit_transcript(a,b)['passed'])
    def test_asr_timing_fails(self):
        a = [{'start':0,'end':1,'text':'数値を確認'}]
        b = [{'start':2,'end':3,'text':'数値を確認'}]
        self.assertFalse(audit_transcript(a,b)['passed'])
    def test_publication_never_allowed(self):
        with self.assertRaises(PermissionError): publication_gate({'status':STATUS})

if __name__ == '__main__': unittest.main()
