import unittest
from table_state import GENRES, frame_state

class TestTableState(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES), 10)

    def test_progress(self):
        self.assertLess(frame_state(5)[0], frame_state(75)[0])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            frame_state(5, rows=(-1,))
