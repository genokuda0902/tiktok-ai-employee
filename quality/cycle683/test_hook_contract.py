import unittest
from hook_contract import GENRES, Hook, validate_hook, allow_publication

class HookContractTests(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            self.assertTrue(validate_hook(Hook(genre, "まだ手で足してる？", "120+150+200+180=650", (110, 1390, 1000, 1520))))
    def test_bad_position(self):
        with self.assertRaises(ValueError):
            validate_hook(Hook("ai_productivity", "question", "evidence", (0, 0, 1080, 1920)))
    def test_missing_evidence(self):
        with self.assertRaises(ValueError):
            validate_hook(Hook("ai_productivity", "question", "", (110, 1390, 1000, 1520)))
    def test_publication_blocked(self):
        self.assertFalse(allow_publication(japanese_voice=False, speech_sync=False, rights=True, human_approval=False))
if __name__ == "__main__":
    unittest.main()
