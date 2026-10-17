"""No-network CI tests for 10-genre Japanese subtitle contract."""
import unittest
from src.quality.script_caption_contract import GENRES, split_caption, validate_script_contract

class ScriptContractTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(set(GENRES)), 10)

    def test_exact_japanese_text(self):
        for s in ("これ、ただの基板じゃありません。",
                  "モニターにつなげば、画面で操作できます。",
                  "入力して、処理して、結果を出す。"):
            a, b = split_caption(s)
            self.assertEqual(a + b, s)
            self.assertLessEqual(max(len(a), len(b)), 16)

    def test_overflow_rejected(self):
        with self.assertRaises(ValueError):
            split_caption("あ" * 40)

    def test_scene_contract(self):
        result = validate_script_contract([
            {"scene": 1, "start": 0, "end": 1.5, "spoken_text": "これはテストです。"},
            {"scene": 2, "start": 1.5, "end": 3, "spoken_text": "日本語字幕を表示します。"},
        ])
        self.assertTrue(all(r["script_exact"] for r in result))

    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            validate_script_contract([
                {"scene": 1, "start": 0, "end": 2, "spoken_text": "開始"},
                {"scene": 2, "start": 1, "end": 3, "spoken_text": "重複"},
            ])

if __name__ == "__main__":
    unittest.main()
