"""Offline regression tests for 10-genre pause-aware captions."""
import tempfile
import unittest
from pathlib import Path
from pause_aware import Caption, GENRES, ass_time, parse_time, parse_silences, voice_ranges, retime, overlap_duration, parse_ass, write_ass

class PauseAwareTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(set(GENRES)), 10)
    def test_timestamp_roundtrip(self): self.assertAlmostEqual(parse_time(ass_time(23.03)), 23.03, places=2)
    def test_parse_silence(self): self.assertEqual(parse_silences('silence_start: 1.0\nsilence_end: 1.5 | silence_duration: 0.5', 3), [(1., 1.5)])
    def test_reject_unpaired_silence(self):
        with self.assertRaises(ValueError): parse_silences('silence_start: 1.0', 3)
    def test_reject_overlap(self):
        with self.assertRaises(ValueError): parse_silences('silence_start: 1\nsilence_end: 2\nsilence_start: 1.5\nsilence_end: 2.5', 3)
    def test_voice_range(self): self.assertEqual(len(voice_ranges([(0, .3), (1., 1.5)], 2)), 2)
    def test_pause_reduction(self):
        old = [Caption(0., 2., '日本語字幕')]
        new = retime(old, [(.8, 1.3)], 2.)
        self.assertLess(overlap_duration(new, [(.8, 1.3)]), overlap_duration(old, [(.8, 1.3)]))
    def test_preserve_text(self):
        old = [Caption(.2, 1.9, '文章A'), Caption(2., 3., '文章B')]
        new = retime(old, [(0., .2), (1.2, 1.5)], 3.)
        self.assertEqual(set(c.text for c in old), set(c.text for c in new))
    def test_reject_bad_caption(self):
        with self.assertRaises(ValueError): retime([Caption(-1., 1., 'bad')], [], 2.)
    def test_no_new_speech_claim(self): self.assertNotIn('ASR', '音声活動検出')
    def test_write_and_read_ass(self):
        h = '[Script Info]\nPlayResX: 1080\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.ass'
            write_ass(p, h, [Caption(.2, .8, '日本語')])
            _, c = parse_ass(p.read_text())
            self.assertEqual(len(c), 1)
            self.assertIn('日本語', c[0].text)
    def test_no_posting_code(self):
        import pause_aware
        s=Path(pause_aware.__file__).read_text()
        self.assertNotIn('requests.post(', s)
        self.assertNotIn('upload_video(', s)

if __name__ == '__main__': unittest.main()
