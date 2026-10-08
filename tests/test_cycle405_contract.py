import unittest

GENRES = ['AI時短','仕事効率化','Excel','営業','学習','暮らし','旅行','料理','健康情報','趣味']

class TestCycle405(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(len(set(GENRES)), 10)

if __name__ == '__main__':
    unittest.main()
