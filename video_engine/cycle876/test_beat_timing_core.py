"""Offline unit tests for cycle876 shared timing core."""
import unittest
from video_engine.cycle876.beat_timing_core import (
    GENRES, STAGE_LABELS, validate_beats, phrase_events, navigation_state
)


def fixture():
    return [
        {"start": i * 0.9, "end": i * 0.9 + 0.7, "text": f"言葉{i}"}
        for i in range(24)
    ]


class BeatTimingTests(unittest.TestCase):
    def test_24_beats(self):
        self.assertTrue(validate_beats(fixture()))
        events = phrase_events(fixture())
        self.assertEqual(len(events), 24)
        self.assertIn("pos(540,1570)", events[0])

    def test_missing_beat_rejected(self):
        with self.assertRaises(ValueError):
            validate_beats(fixture()[:-1])

    def test_overlap_rejected(self):
        data = fixture()
        data[1]["start"] = data[0]["end"] - 0.01
        with self.assertRaises(ValueError):
            validate_beats(data)

    def test_text_sanitized(self):
        data = fixture()
        data[0]["text"] = "{safe}"
        self.assertNotIn("{safe}", phrase_events(data)[0])

    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            for stage in range(1, 9):
                state = navigation_state(stage, genre)
                self.assertEqual(sum(state["filled"]), stage)
                self.assertEqual(state["label"], STAGE_LABELS[stage-1])

    def test_invalid_genre_and_stage(self):
        with self.assertRaises(ValueError):
            navigation_state(1, "unknown")
        with self.assertRaises(ValueError):
            navigation_state(9, GENRES[0])


if __name__ == "__main__":
    unittest.main()
