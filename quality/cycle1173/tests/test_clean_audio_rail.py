import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import clean_audio_rail as q

class RailTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(q.ACCENTS),10)
    def test_all_genres_render(self):
        for g in q.ACCENTS:
            with self.subTest(genre=g):
                s=q.filtergraph(g,23.033333)
                self.assertIn('overlay=',s)
                self.assertIn('drawbox=',s)
    def test_unknown_genre_fails(self):
        with self.assertRaises(ValueError): q.filtergraph('unsupported',23)
    def test_invalid_duration_fails(self):
        with self.assertRaises(ValueError): q.filtergraph('ai',0)
    def test_subtitles_outside_roi(self):
        self.assertGreaterEqual(q.CLEAN_ROI[1],q.CAPTION_SAFE_BOTTOM)
    def test_progress_animated(self):
        self.assertIn('eval=frame',q.filtergraph('ai',23))
    def test_policy_explicit(self): self.assertIn('PUBLICATION_NOT_APPROVED',q.POLICY)
    def test_manifest_hash_fail_closed(self):
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'synthetic'); f.flush()
            m={'policy':q.POLICY,'asset_approval':'review_only_no_publication',
               'manual_post_only':True,'roi_reviewed':True,'genre':'ai',
               'caption_safe_bottom':q.CAPTION_SAFE_BOTTOM,'source_sha256':'wrong'}
            with self.assertRaises(ValueError): q.validate(m,f.name)

if __name__=='__main__': unittest.main()
