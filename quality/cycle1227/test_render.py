import unittest
from render import filters

class TestEvidenceCards(unittest.TestCase):
    def test_three_cards(self):
        self.assertEqual(filters().count("drawtext="), 3)

    def test_distinct_reveals(self):
        for start in (7, 9, 11):
            self.assertIn(f"between(t,{start},14)", filters())

    def test_no_unapproved_asset_loading(self):
        self.assertNotIn("movie=", filters())

if __name__ == "__main__":
    unittest.main()
