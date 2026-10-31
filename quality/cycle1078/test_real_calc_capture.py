import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from .real_calc_capture import (
    FPS,SCENE_START_FRAME,SCENE_END_FRAME,CAPTION_SAFE_Y,TARGET,
    PALETTES,filtergraph,sha256,render
)
class RealCalcCaptureTests(unittest.TestCase):
    def test_scene_is_82_frames(self):
        self.assertEqual(SCENE_END_FRAME-SCENE_START_FRAME,82)
    def test_timeline_exact(self):
        self.assertEqual(SCENE_START_FRAME/FPS,5.8)
        self.assertAlmostEqual(SCENE_END_FRAME/FPS,8.533333,places=5)
    def test_caption_island_safe(self):
        self.assertLess(TARGET[1]+TARGET[3],CAPTION_SAFE_Y)
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES),10)
    def test_unique_palette(self):
        self.assertEqual(len(set(PALETTES.values())),10)
    def test_all_genre_graphs(self):
        for genre in PALETTES:
            with self.subTest(genre=genre):
                g=filtergraph(genre,'/tmp/header','/tmp/detail')
                self.assertIn(PALETTES[genre],g)
                self.assertIn('eof_action=pass',g)
                self.assertIn('setpts=PTS-STARTPTS+5.8/TB',g)
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):filtergraph('unknown','/tmp/header','/tmp/detail')
    def test_hash(self):
        with TemporaryDirectory() as td:
            p=Path(td)/'a';p.write_bytes(b'abc')
            self.assertEqual(sha256(p),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
    def test_missing_files_fail_closed(self):
        with self.assertRaises(FileNotFoundError):render('/no-source','/no-capture','/tmp/out','x','y')
    def test_no_audio_from_capture(self):
        g=filtergraph('ai_work','/tmp/header','/tmp/detail')
        self.assertIn('[1:v]',g)
        self.assertNotIn('[1:a]',g)
    def test_real_capture_required(self):
        self.assertIn('1440,900',Path(__file__).with_name('real_calc_capture.py').read_text())
    def test_no_publishing_calls(self):
        src=Path(__file__).with_name('real_calc_capture.py').read_text()
        for forbidden in ('tiktok.com/upload','api.tiktok.com','requests.post('):
            self.assertNotIn(forbidden,src)
if __name__=='__main__':unittest.main()
