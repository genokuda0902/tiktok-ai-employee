"""Offline tests: ten-genre, safe-zone, provenance, AV-preserving command."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from evidence_insert import (
    GENRES, TOTAL_FRAMES, scene_window, validate_manifest, build_command,
)

GOOD = {'source_kind':'local_gui_capture', 'data_classification':'fictional',
        'contains_personal_data':False, 'review_only':True,
        'publication_approved':False}

class EvidenceTests(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES:
            self.assertEqual(scene_window(g,4),(384,482))
    def test_all_scenes_sum(self):
        self.assertEqual(TOTAL_FRAMES,775)
        for g in GENRES:
            self.assertEqual(scene_window(g,7)[1],775)
    def test_invalid_scene(self):
        for scene in (-1,8,'4'):
            with self.assertRaises(ValueError):scene_window('ai_work',scene)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):scene_window('not_a_genre',4)
    def test_safe_caption_zone(self):
        for bad in [(62,390,1018,1452),(62,390,1018,1400),(-1,390,1018,1390)]:
            with self.assertRaises(ValueError):scene_window('ai_work',4,bad)
    def test_provenance_required(self):
        validate_manifest(GOOD)
        validate_manifest({**GOOD,'source_kind':'synthetic_test_pattern'})
        for key,value in [('data_classification','confidential'),('review_only',False),
                          ('contains_personal_data',True),('publication_approved',True),
                          ('source_kind','unknown')]:
            invalid={**GOOD,key:value}
            with self.assertRaises(ValueError):validate_manifest(invalid)
        with self.assertRaises(ValueError):validate_manifest({})
    def test_inputs_required(self):
        with self.assertRaises(FileNotFoundError):
            build_command(Path('/no-source.mp4'),Path('/no-capture.mp4'),
                          Path('/out.mp4'),'ai_work',4,GOOD)
    def test_short_capture_fails_closed(self):
        with TemporaryDirectory() as td:
            p=Path(td);s=p/'s.mp4';c=p/'c.mp4';s.write_bytes(b'x');c.write_bytes(b'x')
            with patch('evidence_insert.video_duration',return_value=1.0):
                with self.assertRaises(ValueError):
                    build_command(s,c,p/'o.mp4','ai_work',4,GOOD)
    def test_preserves_audio_and_frame_count(self):
        with TemporaryDirectory() as td:
            p=Path(td);s=p/'s.mp4';c=p/'c.mp4';s.write_bytes(b'x');c.write_bytes(b'x')
            with patch('evidence_insert.video_duration',return_value=5.0):
                cmd=build_command(s,c,p/'o.mp4','ai_work',4,GOOD)
            self.assertIn('0:a:0',cmd)
            self.assertIn('copy',cmd)
            self.assertIn('775',cmd)
            self.assertNotIn('upload',cmd)
    def test_no_overwrite(self):
        with TemporaryDirectory() as td:
            p=Path(td);s=p/'s.mp4';c=p/'c.mp4';s.write_bytes(b'x');c.write_bytes(b'x')
            with self.assertRaises(ValueError):
                build_command(s,c,s,'ai_work',4,GOOD)

if __name__=='__main__':unittest.main()
