import unittest
from chapter_overlay import chapter

class ChapterTests(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual([chapter(t) for t in (0, 1.5, 5, 9)],
                         ["課題を確認", "操作を実演", "結果を確認", "手順を復習"])
    def test_end(self):
        self.assertEqual(chapter(11.99), "手順を復習")

if __name__ == "__main__":
    unittest.main()
