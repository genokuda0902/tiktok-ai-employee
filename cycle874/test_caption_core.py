import json
from pathlib import Path
import unittest
from caption_core import GENRES, captions_from_beats, ass_document, dwell_stats

BEATS = json.loads((Path(__file__).parent / "caption_beats.json").read_text(encoding="utf-8"))

class CaptionTests(unittest.TestCase):
    def test_eight_sentences(self):
        self.assertEqual(len(captions_from_beats(BEATS)), 8)
    def test_exact_text_integrity(self):
        captions = captions_from_beats(BEATS)
        self.assertEqual("".join(c.text for c in captions), "".join(b["text"] for b in BEATS))
    def test_dwell_triples(self):
        stats = dwell_stats(captions_from_beats(BEATS), BEATS)
        self.assertEqual(stats["old_events"], 24)
        self.assertEqual(stats["new_events"], 8)
        self.assertGreaterEqual(stats["dwell_multiplier"], 2.9)
    def test_mobile_line_lengths(self):
        self.assertTrue(all(max(map(len, c.lines)) <= 16 for c in captions_from_beats(BEATS)))
    def test_ass_eight_events(self):
        doc = ass_document(captions_from_beats(BEATS))
        self.assertEqual(doc.count("Dialogue:"), 8)
        self.assertEqual(doc.count("\\fad(100,100)"), 8)
    def test_reject_wrong_text(self):
        beats = [dict(b) for b in BEATS]
        beats[1]["text"] = "incorrect"
        with self.assertRaises(ValueError):
            captions_from_beats(beats)
    def test_reject_missing_beat(self):
        with self.assertRaises(ValueError):
            captions_from_beats(BEATS[:-1])
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            self.assertEqual(len(captions_from_beats(BEATS, genre)), 8)
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):
            captions_from_beats(BEATS, "unknown")
    def test_no_caption_overlap(self):
        c = captions_from_beats(BEATS)
        self.assertTrue(all(c[i].end < c[i+1].start for i in range(7)))

if __name__ == "__main__":
    unittest.main()
