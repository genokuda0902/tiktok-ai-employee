import unittest
from photo_contract import GENRES, STATUS, VisualContract, japanese_lines, assert_approved_for_posting

class Cycle807ContractTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(len(set(GENRES)), 10)
        for genre in GENRES:
            self.assertTrue(VisualContract(genre).validate())

    def test_portrait_safety(self):
        with self.assertRaises(ValueError):
            VisualContract("sales_business", width=720).validate()
        with self.assertRaises(ValueError):
            VisualContract("sales_business", photo_rights_review_required=False).validate()
        with self.assertRaises(ValueError):
            VisualContract("sales_business", auto_post=True).validate()

    def test_japanese_caption_wrap_no_orphan(self):
        sentence = "仕事ができる人は、質問が違う。"
        lines = japanese_lines(sentence, lambda s: len(s) * 10, 100)
        self.assertEqual("".join(lines), sentence)
        self.assertEqual(len(lines), 2)
        self.assertTrue(all(line[0] not in "。、" for line in lines))
        self.assertTrue(all(len(line) <= 10 for line in lines))

    def test_short_caption_and_fail_closed(self):
        self.assertEqual(japanese_lines("今日やる。", lambda s: len(s)*10, 100), ["今日やる。"])
        with self.assertRaises(ValueError):
            japanese_lines("", lambda s: len(s), 100)
        with self.assertRaises(ValueError):
            japanese_lines("長い文字列を含むため分割が不可能です。", lambda s: len(s)*10, 10)

    def test_manual_posting_gate(self):
        c = VisualContract("sales_business")
        with self.assertRaises(PermissionError):
            assert_approved_for_posting(c)
        with self.assertRaises(PermissionError):
            assert_approved_for_posting(c, employee_signed_off=True)
        self.assertTrue(assert_approved_for_posting(c, True, True))
        self.assertIn("NOT_APPROVED", STATUS)

if __name__ == "__main__":
    unittest.main()
