import unittest
from loop_contract import GENRES, validate_loop

class TestLoop(unittest.TestCase):
    def test_ten_genres(self):
        for g in GENRES:
            self.assertTrue(validate_loop(g, [(0,2,'hook'),(2,18,'proof'),(18,19,'save'),(19,20,'hook')]))

if __name__ == '__main__': unittest.main()
