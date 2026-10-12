import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "quality" / "cycle514"))
from proof_timeline import BEATS, GENRES, beat_at, validate, validate_timeline

M = json.loads((ROOT / "quality" / "cycle514" / "manifest.json").read_text(encoding="utf8"))

class ProofTimelineTests(unittest.TestCase):
    def test_timeline(self): self.assertTrue(validate_timeline())
    def test_four_beats(self): self.assertEqual(len(BEATS), 4)
    def test_exact_window(self): self.assertEqual((beat_at(2.5),beat_at(6.3),beat_at(7.5)),("pain","verify",None))
    def test_math(self): self.assertEqual(sum(validate(M)["values"]),720)
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_genre_gate(self):
        with self.assertRaises(ValueError): validate({**M,"genre":"unlisted"})
    def test_auto_post_gate(self):
        with self.assertRaises(ValueError): validate({**M,"auto_post":True})
    def test_rights_gate(self):
        with self.assertRaises(ValueError): validate({**M,"rights":"unknown"})
    def test_privacy_gate(self):
        with self.assertRaises(ValueError): validate({**M,"privacy_checked":False})
    def test_false_result_gate(self):
        with self.assertRaises(ValueError): validate({**M,"values":[120,150,200,251]})
    def test_no_publication(self):
        with self.assertRaises(ValueError): validate({**M,"publication":"APPROVED"})

if __name__ == "__main__": unittest.main()
