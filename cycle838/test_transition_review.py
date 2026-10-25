import unittest
from pathlib import Path
from cycle838.transition_review import (GENRES,FRAMES,PHOTO_RECT,CAPTION_RECT,
    TRANSITION_FRAMES,REQUIRED,validate,overlay_graph,run)
from cycle838.audio_gap_audit import parse_intervals

class ReviewTransitionTests(unittest.TestCase):
    def test_ten_genres_share_frame_boundaries(self):
        for genre in GENRES:
            self.assertEqual(validate(genre,REQUIRED),(101,194,285,384,482,583,672))
    def test_scene_plan_unchanged(self):
        self.assertEqual(sum(FRAMES),775)
        self.assertEqual(len(FRAMES),8)
    def test_protected_caption_geometry(self):
        self.assertLess(PHOTO_RECT[3],CAPTION_RECT[1])
        self.assertLessEqual(CAPTION_RECT[3],1920)
    def test_transition_duration_under_half_second(self):
        self.assertLess(TRANSITION_FRAMES/30,.5)
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):validate('unknown',REQUIRED)
    def test_reject_missing_manifest(self):
        with self.assertRaises(ValueError):validate('ai_work',{})
    def test_reject_personal_data(self):
        with self.assertRaises(ValueError):validate('ai_work',{**REQUIRED,'contains_personal_data':True})
    def test_reject_publication_approval_claim(self):
        with self.assertRaises(ValueError):validate('ai_work',{**REQUIRED,'publication_approved':True})
    def test_reject_rights_claim_without_review(self):
        with self.assertRaises(ValueError):validate('ai_work',{**REQUIRED,'source_rights_reviewed':True})
    def test_reject_external_upload(self):
        with self.assertRaises(ValueError):validate('ai_work',{**REQUIRED,'external_upload':True})
    def test_reject_auto_post(self):
        with self.assertRaises(ValueError):validate('ai_work',{**REQUIRED,'automatic_posting':True})
    def test_reject_boolean_frames(self):
        with self.assertRaises(ValueError):validate('ai_work',REQUIRED,True)
    def test_reject_long_transition(self):
        with self.assertRaises(ValueError):validate('ai_work',REQUIRED,15)
    def test_reject_short_transition(self):
        with self.assertRaises(ValueError):validate('ai_work',REQUIRED,2)
    def test_seven_alpha_dissolves(self):
        g=overlay_graph(validate('ai_work',REQUIRED))
        self.assertEqual(g.count('fade=t=out'),7)
        self.assertEqual(g.count('overlay=62:390'),7)
        self.assertEqual(g.count('repeatlast=0'),7)
        self.assertIn('format=yuv420p[vout]',g)
    def test_refuse_missing_source(self):
        with self.assertRaises(FileNotFoundError):
            run(Path('/nonexistent/private.mp4'),Path('/tmp/never.mp4'),'ai_work',REQUIRED)
    def test_parse_silence_intervals(self):
        log='silence_start: 1.2\nsilence_end: 2.05 | silence_duration: 0.85'
        self.assertEqual(parse_intervals(log),[(1.2,2.05)])
    def test_ignore_unpaired_silence_start(self):
        self.assertEqual(parse_intervals('silence_start: 3.2'),[])

if __name__=='__main__':unittest.main()
