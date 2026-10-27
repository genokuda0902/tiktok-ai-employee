import unittest
from pathlib import Path
import tempfile
from caption_legibility import select_font_size, text_without_ass_tags, upgrade_ass, validate_reading_groups, GENRES

class CaptionTests(unittest.TestCase):
    def test_strips_ass_formatting(self):
        self.assertEqual(text_without_ass_tags('{\\c&H00FFFFFF&}日本語\\N字幕'), '日本語\n字幕')
    def test_font_grows_when_fits(self):
        self.assertEqual(select_font_size(['テスト'], lambda s, n: len(s)*n), 71)
    def test_font_shrinks_to_fit(self):
        self.assertEqual(select_font_size(['テスト'], lambda s, n: n*13), 70)
    def test_font_rejects_overflow(self):
        with self.assertRaises(ValueError): select_font_size(['長文'], lambda s,n: 9999)
    def test_empty_rejected(self):
        with self.assertRaises(ValueError): select_font_size([''], lambda s,n: 0)
    def test_10_genres(self):
        self.assertEqual(len(GENRES), 10)
    def test_unsupported_genre(self):
        with tempfile.TemporaryDirectory():
            with self.assertRaises(ValueError): upgrade_ass('missing','missing',lambda s,n:0,genre='unapproved')
    def test_reading_group_joins_karaoke(self):
        data=[{'start':'0:00:01.00','end':'0:00:01.50','text':'日本語'}, {'start':'0:00:01.50','end':'0:00:02.00','text':'日本語'}]
        groups=validate_reading_groups(data)
        self.assertEqual(len(groups),1)
        self.assertEqual(groups[0]['chars_per_second'],3.0)
    def test_reading_group_does_not_join_gap(self):
        data=[{'start':'0:00:01.00','end':'0:00:01.50','text':'日本語'}, {'start':'0:00:01.80','end':'0:00:02.00','text':'日本語'}]
        self.assertEqual(len(validate_reading_groups(data)),2)
    def test_source_integrity_and_24_cues(self):
        src=Path(__file__).parent/'captions_original.ass'
        if not src.exists(): self.skipTest('source not present in standalone CI')
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'new.ass'
            decisions=upgrade_ass(src,out,lambda s,n:len(s)*n*.9)
            self.assertEqual(len(decisions),24)
            self.assertIn('{\\fs71}',out.read_text())
            self.assertEqual(out.read_text().count('Dialogue:'),24)

if __name__ == '__main__': unittest.main()
