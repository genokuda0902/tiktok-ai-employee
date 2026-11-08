import unittest

CAPTIONS = [(0, 3, "集計、まだ手作業？"), (3, 6, "合計を出したいセルを選択"), (6, 9, "=SUM(B2:B4) と入力"), (9, 12, "12,000円と表示されたら完成")]

class CaptionTimelineTests(unittest.TestCase):
    def test_no_gaps_or_overlaps(self):
        self.assertEqual(CAPTIONS[0][0], 0)
        self.assertEqual(CAPTIONS[-1][1], 12)
        for previous, following in zip(CAPTIONS, CAPTIONS[1:]):
            self.assertEqual(previous[1], following[0])
    def test_japanese_present(self):
        for _, _, text in CAPTIONS:
            self.assertTrue(any("\\u3040" <= c <= "\\u9fff" for c in text))

if __name__ == "__main__":
    unittest.main()
