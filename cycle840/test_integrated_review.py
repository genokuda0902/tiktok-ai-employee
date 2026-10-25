"""Synthetic/unit-only tests: never use private footage in CI."""
import unittest
from copy import deepcopy
from cycle840.integrated_review import REQUIRED, validate_manifest, av_metrics, assert_av, CANONICAL_GENRES, PACING_ALIASES
from cycle839.pacing import GENRES

VALID={**REQUIRED,'source_sha256':'a'*64}

def metadata(audio_seconds=25.833, frames=775):
    return {'streams':[
        {'codec_type':'video','codec_name':'h264','width':1080,'height':1920,
         'r_frame_rate':'30/1','nb_frames':str(frames)},
        {'codec_type':'audio','codec_name':'aac','sample_rate':'48000','duration':str(audio_seconds)}],
        'format':{'duration':str(frames/30)}}

class IntegrationSafety(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(CANONICAL_GENRES),10)
        for genre in CANONICAL_GENRES:validate_manifest(VALID,genre)
    def test_legacy_genre_alias(self):
        self.assertEqual(PACING_ALIASES["productivity"],"product_comparison_lifestyle")
        validate_manifest(VALID,"productivity")
        with self.assertRaises(ValueError):validate_manifest(VALID,"product_comparison_lifestyle")
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):validate_manifest(VALID,'made_up')
    def test_reject_unapproved_upload_or_post(self):
        for k in ('external_upload','automatic_posting','publication_approved','source_rights_reviewed'):
            bad=deepcopy(VALID);bad[k]=True
            with self.subTest(k=k),self.assertRaises(ValueError):validate_manifest(bad,'ai_work')
    def test_reject_untrusted_source(self):
        for k in ('contains_cycle838_dissolves','review_only','source_sha256'):
            bad=deepcopy(VALID);bad.pop(k)
            with self.subTest(k=k),self.assertRaises(ValueError):validate_manifest(bad,'ai_work')
    def test_reject_personal_data(self):
        bad=deepcopy(VALID);bad['contains_personal_data']=True
        with self.assertRaises(ValueError):validate_manifest(bad,'ai_work')
    def test_full_length_audio_valid(self):
        v,a,d=av_metrics(metadata())
        self.assertEqual(v['nb_frames'],'775')
        self.assertAlmostEqual(float(a['duration']),d,places=2)
    def test_short_audio_must_fail(self):
        from unittest.mock import patch
        with patch('cycle840.integrated_review.probe',return_value=metadata(audio_seconds=0.704)):
            with self.assertRaisesRegex(ValueError,'Audio incomplete'):
                assert_av('fixture.mp4',775)
    def test_output_duration_valid(self):
        from unittest.mock import patch
        with patch('cycle840.integrated_review.probe',return_value=metadata(audio_seconds=23.0,frames=691)):
            self.assertEqual(assert_av('fixture.mp4',691)['frames'],691)
    def test_reject_wrong_resolution(self):
        bad=metadata();bad['streams'][0]['width']=720
        with self.assertRaises(ValueError):av_metrics(bad)
    def test_reject_missing_audio(self):
        bad=metadata();bad['streams'].pop()
        with self.assertRaises(ValueError):av_metrics(bad)

if __name__=='__main__':unittest.main()
