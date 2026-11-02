import importlib.util
import tempfile
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'code'/'chapter_tail_pacing.py'
spec=importlib.util.spec_from_file_location('chapter_tail_pacing',P)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class TailTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(mod.GENRES),10)
        self.assertEqual(len(set(mod.GENRES)),10)
    def test_tail_trims_with_postroll(self):
        cut,reason=mod.calculate_cut(22.5,30,[(22.0,22.515)],19.167)
        self.assertEqual(cut,22.2)
        self.assertEqual(reason,'trimmed_trailing_silence')
    def test_short_pause_not_trimmed(self):
        cut,_=mod.calculate_cut(22.5,30,[(22.2,22.515)],19.167)
        self.assertEqual(cut,22.5)
    def test_interior_pause_not_trimmed(self):
        cut,_=mod.calculate_cut(22.5,30,[(21.1,21.5)],19.167)
        self.assertEqual(cut,22.5)
    def test_last_chapter_protected(self):
        cut,_=mod.calculate_cut(22.5,30,[(22.0,22.515)],21.8)
        self.assertEqual(cut,22.5)
    def test_no_silence(self):
        cut,_=mod.calculate_cut(22.5,30,[],19)
        self.assertEqual(cut,22.5)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError): mod.optimize('x','y',genre='invalid')
    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError): mod.optimize('x','y')
    def test_same_file(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.mp4';p.write_bytes(b'bad')
            with self.assertRaises(ValueError):mod.optimize(p,p)
    def test_ffmpeg_failure(self):
        with self.assertRaises(RuntimeError):mod.call(['ffmpeg','-invalid-option'])
if __name__=='__main__': unittest.main()
