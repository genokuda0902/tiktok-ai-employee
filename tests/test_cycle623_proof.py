import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "quality" / "cycle623"))
from proof_contract import Proof, GENRES, scene_at, in_safe_area

class ProofContractTests(unittest.TestCase):
    def test_genres(self):
        for genre in GENRES:
            self.assertEqual(Proof(genre=genre).validate()["sum"], 720)
    def test_arithmetic(self):
        self.assertEqual(Proof(values=(1,2,3,4)).validate()["sum"], 10)
    def test_formula(self):
        self.assertEqual(Proof().validate()["formula"], "=SUM(B2:B5)")
    def test_bad_values(self):
        for vals in [(1,2,3), (1,2,3,-1), (1,2,3,"4")]:
            with self.assertRaises(ValueError): Proof(values=vals).validate()
    def test_bad_genre(self):
        with self.assertRaises(ValueError): Proof(genre="unknown").validate()
    def test_rights_fail_closed(self):
        with self.assertRaises(ValueError): Proof(rights="UNKNOWN").validate()
    def test_publication_fail_closed(self):
        with self.assertRaises(ValueError): Proof(publication="APPROVED").validate()
        with self.assertRaises(ValueError): Proof(auto_post=True).validate()
    def test_voice_truth(self):
        with self.assertRaises(ValueError): Proof(japanese_narration="VERIFIED").validate()
        with self.assertRaises(ValueError): Proof(actual_excel_recording=True).validate()
    def test_scene_timeline(self):
        self.assertEqual(scene_at(11), "range_selection")
        self.assertEqual(scene_at(13), "formula_and_total")
        self.assertEqual(scene_at(15), "four_bar_chart")
        with self.assertRaises(ValueError): scene_at(16.5)
    def test_safe_bounds(self):
        self.assertTrue(in_safe_area((60,100,1000,1650)))
        self.assertFalse(in_safe_area((60,100,1000,1900)))

if __name__ == "__main__":
    unittest.main()
