"""Offline regression tests for duplicate-free, 10-genre subtitle layout."""
import unittest
from video_engine.cycle877.single_track_caption_core import (
    GENRES, CAPTION_PANEL, CAPTION_CENTER, events, make_ass,
    phrase_text, validate_layout, escape_ass
)


def fixture():
    beats = []
    lines = []
    for i in range(8):
        lines.append(("最初に", "確認する"))
        for j, word in enumerate(("最初", "に", "確認する")):
            index = 3*i+j
            beats.append({"start": index*0.9, "end": index*0.9+0.7, "text": word})
    return beats, lines


class SingleTrackTests(unittest.TestCase):
    def test_24_events_no_duplicate_layer(self):
        beats, lines = fixture()
        result = events(beats, lines)
        self.assertEqual(len(result), 24)
        self.assertTrue(all(s.startswith("Dialogue: 0,") for s in result))
        self.assertTrue(all(s.count(r"\N") == 1 for s in result))

    def test_single_style_only(self):
        beats, lines = fixture()
        ass = make_ass(beats, lines)
        self.assertEqual(ass.count("Dialogue:"), 24)
        self.assertNotIn("Style: BEAT", ass)
        self.assertNotIn("Dialogue: 1,", ass)
        self.assertIn(r"\pos(540,1554)", ass)

    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            self.assertTrue(validate_layout(genre))

    def test_exact_sentence_preserved(self):
        beats, lines = fixture()
        for i in range(8):
            group = beats[3*i:3*i+3]
            for active in range(3):
                highlighted = phrase_text(group, *lines[i], active)
                self.assertIn(r"{\c&H0000F9FF&}", highlighted)
                self.assertIn(r"\N", highlighted)

    def test_invalid_beat_count(self):
        beats, lines = fixture()
        with self.assertRaises(ValueError):
            events(beats[:-1], lines)

    def test_overlap_rejected(self):
        beats, lines = fixture()
        beats[1]["start"] = beats[0]["end"] - 0.1
        with self.assertRaises(ValueError):
            events(beats, lines)

    def test_text_mismatch_rejected(self):
        beats, lines = fixture()
        lines[0] = ("間違い", "文章")
        with self.assertRaises(ValueError):
            events(beats, lines)

    def test_too_long_line_rejected(self):
        beats, lines = fixture()
        lines[0] = ("あ"*18, "確認する")
        with self.assertRaises(ValueError):
            events(beats, lines)

    def test_unsafe_genre_rejected(self):
        with self.assertRaises(ValueError):
            validate_layout("unrecognized")

    def test_ass_escaping(self):
        self.assertNotIn("{", escape_ass("{\\an5}"))
        self.assertNotIn("}", escape_ass("{\\an5}"))


if __name__ == "__main__":
    unittest.main()
