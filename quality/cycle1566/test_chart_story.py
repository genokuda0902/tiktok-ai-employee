import unittest
from chart_story import Scene, sample, validate, PUBLICATION_NOT_APPROVED, FICTIONAL_DATA

class TestChartStory(unittest.TestCase):
    def test_sample(self):
        self.assertTrue(validate(sample()))
        self.assertEqual(sum(x.seconds for x in sample()), 20)
    def test_negative_bar(self):
        with self.assertRaises(ValueError):
            validate([Scene("a","b",(("bad",-1),))])
    def test_no_approval(self):
        self.assertTrue(PUBLICATION_NOT_APPROVED)
        self.assertTrue(FICTIONAL_DATA)

if __name__ == "__main__":
    unittest.main()
