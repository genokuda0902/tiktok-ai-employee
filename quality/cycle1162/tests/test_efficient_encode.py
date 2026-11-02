import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from efficient_encode import (POLICY, GENRES, MAX_SIZE_RATIO, FULL_SSIM_MIN,
                              CAPTION_SSIM_MIN, validate_manifest, sha256, ssim)

class TestEncode(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'src.mp4'
        self.path.write_bytes(b'fake source for policy tests')
        self.m = {'policy': POLICY, 'asset_approval': 'review_only_no_publication',
                  'manual_post_only': True, 'genre': 'ai', 'layout_id': 'eight_scene_v1',
                  'source_sha256': sha256(self.path)}
    def tearDown(self): self.temp.cleanup()
    def test_ten_genres(self):
        for g in GENRES:
            self.m['genre'] = g
            validate_manifest(self.m, self.path)
    def test_no_publication(self):
        self.m['policy'] = 'PUBLICATION_APPROVED'
        with self.assertRaises(ValueError): validate_manifest(self.m, self.path)
    def test_no_manual_post_false(self):
        self.m['manual_post_only'] = False
        with self.assertRaises(ValueError): validate_manifest(self.m, self.path)
    def test_no_wrong_sha(self):
        self.m['source_sha256'] = '0' * 64
        with self.assertRaises(ValueError): validate_manifest(self.m, self.path)
    def test_no_unsupported_genre(self):
        self.m['genre'] = 'unsafe'
        with self.assertRaises(ValueError): validate_manifest(self.m, self.path)
    def test_no_wrong_layout(self):
        self.m['layout_id'] = 'unknown'
        with self.assertRaises(ValueError): validate_manifest(self.m, self.path)
    def test_strict_quality_thresholds(self):
        self.assertLessEqual(MAX_SIZE_RATIO, .70)
        self.assertGreaterEqual(FULL_SSIM_MIN, .99)
        self.assertGreaterEqual(CAPTION_SSIM_MIN, .99)
    def test_hash_deterministic(self):
        self.assertEqual(sha256(self.path), hashlib.sha256(self.path.read_bytes()).hexdigest())

if __name__ == '__main__': unittest.main()
