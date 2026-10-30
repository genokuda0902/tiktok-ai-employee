import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'quality'/'cycle1101'))
from step_spotlight import STAGES,CHAPTERS,GENRE_ACCENTS,Stage,RAIL,filtergraph,validate

class RailTests(unittest.TestCase):
    def test_layout(self):self.assertTrue(validate())
    def test_ten_genres(self):self.assertEqual(len(GENRE_ACCENTS),10)
    def test_all_presets_compile(self):
        for genre in GENRE_ACCENTS:self.assertIn('format=yuv420p',filtergraph(genre))
    def test_six_unique_stages(self):self.assertEqual([(s.scene,s.index) for s in STAGES],[(4,1),(4,2),(4,3),(5,1),(5,2),(5,3)])
    def test_chapter_boundaries(self):self.assertEqual(STAGES[0].first,260);self.assertEqual(STAGES[-1].last,421)
    def test_caption_safe(self):self.assertTrue(validate(rail=RAIL))
    def test_timing_overlap_rejected(self):
        bad=list(STAGES);bad[1]=Stage(4,2,280,314)
        with self.assertRaises(ValueError):validate(tuple(bad))
    def test_outside_chapter_rejected(self):
        bad=list(STAGES);bad[2]=Stage(4,3,316,345)
        with self.assertRaises(ValueError):validate(tuple(bad))
    def test_caption_intrusion_rejected(self):
        with self.assertRaises(ValueError):validate(rail=(48,1550,984,94))
    def test_progress_intrusion_rejected(self):
        with self.assertRaises(ValueError):validate(rail=(48,1690,984,94))
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):filtergraph('unknown')
    def test_filters_have_frame_enables(self):
        g=filtergraph()
        for s in STAGES:self.assertIn(f'between(n,{s.first},{s.last})',g)
    def test_no_audio_filters(self):self.assertNotIn('volume=',filtergraph())
    def test_labels_match_source(self):
        self.assertEqual(CHAPTERS[4][2],('目的','条件','形式'))
        self.assertEqual(CHAPTERS[5][2],('数字・根拠','日付・名前','断定表現'))

if __name__=='__main__':unittest.main()
