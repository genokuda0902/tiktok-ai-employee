import unittest
from dataclasses import replace
from pathlib import Path
import tempfile
from kinetic_endcard import (DEFAULT, GENRES, EndCard, REVIEW_POLICY,
                              eased, stage_progress, validate_story, validate_manifest)

class TestEndCard(unittest.TestCase):
    def test_all_ten_genres(self):
        for genre in GENRES: self.assertTrue(validate_story(replace(DEFAULT,genre=genre)))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): validate_story(replace(DEFAULT,genre='unknown'))
    def test_missing_steps(self):
        with self.assertRaises(ValueError): validate_story(replace(DEFAULT,steps=('a','b')))
    def test_empty_headline(self):
        with self.assertRaises(ValueError): validate_story(replace(DEFAULT,headline=''))
    def test_long_headline(self):
        with self.assertRaises(ValueError): validate_story(replace(DEFAULT,headline='長'*40))
    def test_public_url_rejected(self):
        with self.assertRaises(ValueError): validate_story(replace(DEFAULT,cta='https://bad.example'))
    def test_contact_rejected(self):
        with self.assertRaises(ValueError): validate_story(replace(DEFAULT,cta='@username'))
    def test_ease_bounds(self):
        self.assertEqual(eased(-1),0); self.assertEqual(eased(2),1)
    def test_reveal_starts_hidden(self):
        steps,cta=stage_progress(0)
        self.assertEqual(steps,(0,0,0));self.assertEqual(cta,0)
    def test_reveal_ends_visible(self):
        steps,cta=stage_progress(102)
        self.assertEqual(steps,(1,1,1));self.assertEqual(cta,1)
    def test_invalid_frame(self):
        with self.assertRaises(ValueError): stage_progress(103)
    def test_manifest_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'private.mp4'; f.write_bytes(b'test')
            with self.assertRaises(ValueError): validate_manifest(f,dict(REVIEW_POLICY))
    def test_manifest_valid_only_for_review(self):
        from kinetic_endcard import sha256
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'private.mp4'; f.write_bytes(b'test')
            self.assertTrue(validate_manifest(f,{**REVIEW_POLICY,'source_sha256':sha256(f)}))
            with self.assertRaises(ValueError): validate_manifest(f,{**REVIEW_POLICY,'source_sha256':sha256(f),'publication_approved':True})

if __name__=='__main__':unittest.main()
