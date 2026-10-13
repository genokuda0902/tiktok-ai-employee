"""Tests for cycle547 fail-closed scene quality contract."""
import unittest
from quality.cycle547.scene_contract import GENRES, check_scene

BASE = dict(genre="ai_work", asset_status="synthetic_review_only", publication_status="NOT_APPROVED", data_is_real=False, values=[120,150,200,250], total=720)
class SceneTests(unittest.TestCase):
    def test_ten_genres(self):
        for g in GENRES:
            self.assertTrue(check_scene(dict(BASE,genre=g)))
    def test_arithmetic(self):
        with self.assertRaises(ValueError): check_scene(dict(BASE,total=719))
    def test_rights(self):
        with self.assertRaises(ValueError): check_scene(dict(BASE,asset_status="unverified"))
    def test_publication(self):
        with self.assertRaises(ValueError): check_scene(dict(BASE,publication_status="APPROVED"))
    def test_real_data(self):
        with self.assertRaises(ValueError): check_scene(dict(BASE,data_is_real=True))
    def test_invalid_value(self):
        with self.assertRaises(ValueError): check_scene(dict(BASE,values=[120,150,200,-1]))
if __name__=="__main__":unittest.main()
