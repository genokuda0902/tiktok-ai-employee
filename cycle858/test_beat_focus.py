import unittest,tempfile
from pathlib import Path
from beat_focus import GENRES,POLICY,SCENES,CUTS,ROI,plan,validate,sha256

class BeatFocusTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(set(GENRES)),10)
    def test_eight_contiguous_scenes(self):self.assertEqual(SCENES[0][0],0);self.assertEqual(SCENES[-1][1],691);plan()
    def test_six_new_focus_shots(self):self.assertEqual(len(CUTS),6)
    def test_frame_count_changed(self):self.assertEqual(plan()['cut_frames'],298)
    def test_cut_windows_non_overlapping(self):
        for (a,b),(c,d) in zip(CUTS,CUTS[1:]):self.assertLessEqual(b,c)
    def test_caption_safe_roi(self):self.assertLessEqual(ROI[1]+ROI[3],1240)
    def test_no_auto_post(self):self.assertFalse(POLICY['automatic_posting'])
    def test_rights_not_approved(self):self.assertFalse(POLICY['source_rights_reviewed'])
    def test_no_public_upload(self):self.assertFalse(POLICY['external_upload'])
    def test_no_publication(self):self.assertFalse(POLICY['publication_approved'])
    def test_reject_bad_zoom(self):
        with self.assertRaises(ValueError):plan(zoom=1.5)
    def test_reject_caption_overlay(self):
        with self.assertRaises(ValueError):plan(roi=(86,476,908,1000))
    def test_reject_outside_cut(self):
        with self.assertRaises(ValueError):plan(cuts=((700,710),))
    def test_reject_missing_source(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):validate(Path(d)/'missing.mp4',Path(d)/'out.mp4',{},'ai_work',SCENES,CUTS)
    def test_reject_bad_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source.mp4';p.write_bytes(b'fake')
            with self.assertRaises(ValueError):validate(p,Path(d)/'out.mp4',{},'ai_work',SCENES,CUTS)
    def test_reject_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source.mp4';p.write_bytes(b'fake')
            with self.assertRaises(ValueError):validate(p,p,{**POLICY,'source_sha256':sha256(p)},'ai_work',SCENES,CUTS)
    def test_enable_uses_frames(self):self.assertIn('between(n\\,118\\,169)',plan()['enable'])
if __name__=='__main__':unittest.main()
