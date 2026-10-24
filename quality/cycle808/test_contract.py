import unittest
from contract import GENRES, SENTENCES, RenderContract, wrap_japanese, allow_manual_post

class Cycle808Tests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(len(set(GENRES)), 10)
        for genre in GENRES:
            self.assertTrue(RenderContract(genre).validate())

    def test_portrait_format_and_eight_scenes(self):
        for kwargs in ({"width": 720}, {"height": 1280}, {"fps": 25}, {"scenes": 7}):
            with self.assertRaises(ValueError):
                RenderContract("sales_business", **kwargs).validate()

    def test_rights_and_publication_gate(self):
        for kwargs in ({"inherited_voice_license_review": False},
                       {"original_visuals": False}, {"employee_approved": True},
                       {"auto_post": True}):
            with self.assertRaises(ValueError):
                RenderContract("sales_business", **kwargs).validate()
        with self.assertRaises(PermissionError):
            allow_manual_post(RenderContract("sales_business"))
        with self.assertRaises(PermissionError):
            allow_manual_post(RenderContract("sales_business"), employee_signed_off=True)

    def test_japanese_captions(self):
        self.assertEqual(len(SENTENCES), 8)
        for sentence in SENTENCES:
            parts = wrap_japanese(sentence, lambda s: len(s)*10, 105)
            self.assertEqual("".join(parts), sentence)
            self.assertLessEqual(len(parts), 2)
            self.assertTrue(all(p[0] not in "。、）" for p in parts))

    def test_caption_failure(self):
        with self.assertRaises(ValueError):
            wrap_japanese("", len, 10)
        with self.assertRaises(ValueError):
            wrap_japanese("あ"*40, len, 3)

if __name__ == "__main__":
    unittest.main()
