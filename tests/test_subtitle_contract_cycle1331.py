"""Reusable, dependency-free subtitle timeline contract for ten content genres.

Checks structural timing only; it does NOT verify spoken Japanese or semantic match.
Usage: python -m unittest discover -s tests -p 'test_subtitle_contract_cycle1331.py'
"""
import json
import unittest

def validate_cues(cues, duration_ms, max_chars=36):
    errors = []
    if not isinstance(cues, list) or not cues:
        return ["subtitle cues must be a nonempty list"]
    previous_end = 0
    for index, cue in enumerate(cues):
        if not isinstance(cue, dict):
            errors.append(f"cue {index}: not an object")
            continue
        start, end, text = cue.get("start_ms"), cue.get("end_ms"), cue.get("text")
        if not isinstance(start, int) or not isinstance(end, int):
            errors.append(f"cue {index}: integer millisecond timestamps required")
            continue
        if start < previous_end or end <= start or end > duration_ms:
            errors.append(f"cue {index}: overlap, inverted, or out-of-range timing")
        if not isinstance(text, str) or not text.strip() or len(text) > max_chars:
            errors.append(f"cue {index}: empty or overly long subtitle")
        previous_end = end
    return errors

class SubtitleContractTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate_cues([{"start_ms":0,"end_ms":1200,"text":"今日のポイント"}], 2000), [])
    def test_overlap(self):
        cues = [{"start_ms":0,"end_ms":1200,"text":"前半"},{"start_ms":1100,"end_ms":1800,"text":"後半"}]
        self.assertTrue(validate_cues(cues, 2000))
    def test_out_of_bounds(self):
        self.assertTrue(validate_cues([{"start_ms":0,"end_ms":2200,"text":"長すぎ"}], 2000))
    def test_empty(self):
        self.assertTrue(validate_cues([], 2000))
    def test_long(self):
        self.assertTrue(validate_cues([{"start_ms":0,"end_ms":1200,"text":"あ"*40}], 2000))

if __name__ == "__main__":
    unittest.main()
