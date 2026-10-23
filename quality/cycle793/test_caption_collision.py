import json
import unittest
from pathlib import Path
from repair_caption_collision import validate, intersection, GENRES

CFG = json.loads((Path(__file__).parent / 'config.json').read_text(encoding='utf-8'))

class TestCollisionGuard(unittest.TestCase):
    def test_ten_genres(self):
        for g in GENRES: self.assertTrue(validate({**CFG, 'genre': g}))
    def test_overlap_detected(self):
        r = CFG['collision_rules'][0]
        self.assertGreater(intersection(r['caption_box'], r['protected_box']), 0)
    def test_no_overlap_rejected(self):
        r = {**CFG['collision_rules'][0], 'protected_box': [0, 0, 100, 100]}
        with self.assertRaises(ValueError): validate({**CFG, 'collision_rules': [r]})
    def test_bad_band_rejected(self):
        r = {**CFG['collision_rules'][0], 'repair_band': [0, 0, 1080, 100]}
        with self.assertRaises(ValueError): validate({**CFG, 'collision_rules': [r]})
    def test_bad_interval_rejected(self):
        r = {**CFG['collision_rules'][0], 'end': 30}
        with self.assertRaises(ValueError): validate({**CFG, 'collision_rules': [r]})
    def test_no_rights_autoapproval(self):
        with self.assertRaises(ValueError): validate({**CFG, 'rights_reviewed': True})
    def test_no_publication_autoapproval(self):
        with self.assertRaises(ValueError): validate({**CFG, 'publication_approved': True})
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): validate({**CFG, 'genre': 'not_allowed'})
    def test_no_rules(self):
        with self.assertRaises(ValueError): validate({**CFG, 'collision_rules': []})
    def test_valid(self):
        self.assertTrue(validate(CFG))

if __name__ == '__main__': unittest.main()
