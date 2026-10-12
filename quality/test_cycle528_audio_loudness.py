import unittest
from pathlib import Path
from cycle528_audio_loudness import GENRES, check_input, parse_loudnorm

class Cycle528Tests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(set(GENRES)), 10)

    def test_rights(self):
        data = dict(genre=GENRES[0], rights='UNKNOWN', contains_private_data=False, publication='NOT_APPROVED', review_status='HUMAN_REVIEW')
        with self.assertRaises(ValueError):
            check_input(Path(__file__), data)

    def test_privacy(self):
        data = dict(genre=GENRES[0], rights='SYNTHETIC_OR_OWNER_APPROVED', contains_private_data=True, publication='NOT_APPROVED', review_status='HUMAN_REVIEW')
        with self.assertRaises(ValueError):
            check_input(Path(__file__), data)

    def test_measurement(self):
        with self.assertRaises(RuntimeError):
            parse_loudnorm('invalid')

if __name__ == '__main__':
    unittest.main()
