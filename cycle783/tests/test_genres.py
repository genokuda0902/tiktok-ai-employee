import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class GenreConfigTest(unittest.TestCase):
    def test_ten_genres(self):
        data = json.loads((ROOT / "config/genres.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["genres"]), 10)
        self.assertEqual(len({g["name"] for g in data["genres"]}), 10)

if __name__ == "__main__":
    unittest.main()
