"""Cycle788 scene contract regression tests. No external assets or paid services."""
import importlib.util
import pathlib
import unittest

SRC = pathlib.Path(__file__).resolve().parents[1] / "src" / "scene_contract.py"
spec = importlib.util.spec_from_file_location("scene_contract", SRC)
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)

class SceneContractTests(unittest.TestCase):
    def test_shared_contract(self):
        self.assertTrue(contract.validate())
    def test_all_genres(self):
        self.assertEqual(len(contract.GENRES), 10)
        self.assertIn("science", contract.GENRES)
    def test_scene_timing(self):
        self.assertEqual(len(contract.SCENES), 8)
        self.assertEqual(sum(contract.FRAMES), 429)
        self.assertEqual(len(contract.CUES), 16)
    def test_cue_no_overlap(self):
        self.assertTrue(all(
            a[0] < a[1] <= b[0]
            for a, b in zip(contract.CUES, contract.CUES[1:])
        ))
    def test_japanese_content(self):
        self.assertTrue(all(len(s[0]) and len(s[1]) for s in contract.SCENES))
        self.assertEqual(contract.CUES[-1][2], "あとで試そう。")

if __name__ == "__main__":
    unittest.main()
