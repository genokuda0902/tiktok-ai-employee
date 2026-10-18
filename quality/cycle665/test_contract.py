import unittest
from quality.cycle665.contract import caption_matches_script, count_genres

class ContractTests(unittest.TestCase):
    def test_equal_script(self):
        self.assertTrue(caption_matches_script('これは基板です。', 'これは基板です。'))
    def test_reject_editorial_summary(self):
        self.assertFalse(caption_matches_script('小さなPC', 'これは基板です。'))
    def test_genre_count(self):
        self.assertEqual(count_genres(dict.fromkeys(range(10))), 10)

if __name__ == '__main__':
    unittest.main()
