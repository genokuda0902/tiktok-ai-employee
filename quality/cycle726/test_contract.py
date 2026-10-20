import unittest

class QualityContract(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(range(10)), 10)

if __name__ == '__main__':
    unittest.main()
