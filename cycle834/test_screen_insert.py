"""Offline, ten-genre fail-closed tests for real screen recording insertion."""
import unittest
from pathlib import Path
from screen_insert import validate, frame_window, command
from cycle833.focal_layout import GENRES,FRAMES

class ScreenInsertTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES:self.assertEqual(validate(g,2),(194,285))
    def test_all_scenes(self):
        for i in range(8):
            a,b=frame_window(i)
            self.assertEqual(b-a,FRAMES[i])
        self.assertEqual(frame_window(7)[1],775)
    def test_protected_regions(self):
        with self.assertRaises(ValueError):validate('ai_work',2,(62,390,1018,1453))
        with self.assertRaises(ValueError):validate('ai_work',2,(62,390,1018,1401))
    def test_invalid(self):
        with self.assertRaises(ValueError):validate('unknown',2)
        with self.assertRaises(ValueError):validate('ai_work',8)
        with self.assertRaises(ValueError):validate('ai_work',-1)
    def test_file_checks(self):
        with self.assertRaises(FileNotFoundError):
            command(Path('/absent.mp4'),Path('/absent2.mp4'),Path('/tmp/o.mp4'))
    def test_preserve_audio_and_frames(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as td:
            p=Path(td);src=p/'a.mp4';clip=p/'b.mp4';out=p/'c.mp4'
            src.write_bytes(b'fixture');clip.write_bytes(b'fixture')
            cmd=command(src,clip,out)
            self.assertIn('0:a:0',cmd)
            self.assertIn('copy',cmd)
            self.assertIn('775',cmd)
            self.assertNotIn('upload',cmd)

if __name__=='__main__':unittest.main()
