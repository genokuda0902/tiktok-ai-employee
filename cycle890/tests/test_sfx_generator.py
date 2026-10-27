import sys
import tempfile
import unittest
import wave
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from sfx_generator import make_cues, parse_times

class TestCues(unittest.TestCase):
    def test_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            a = make_cues(Path(d)/'a.wav', 2.0, (0.7, 1.4), (0.9,))
            b = make_cues(Path(d)/'b.wav', 2.0, (0.7, 1.4), (0.9,))
            self.assertEqual(a['sha256'], b['sha256'])
            self.assertEqual(a['samples'], 96000)
    def test_valid_wave(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'a.wav'
            q = make_cues(p, 2.0, (0.7,), (0.9,))
            with wave.open(str(p), 'rb') as w:
                self.assertEqual((w.getnchannels(), w.getframerate(), w.getsampwidth()), (1, 48000, 2))
                self.assertEqual(w.getnframes(), 96000)
            self.assertLess(q['cue_peak_dbfs'], -21)
    def test_no_event_is_silent(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'silence.wav'
            make_cues(p, 2.0, (), ())
            with wave.open(str(p), 'rb') as w:
                self.assertEqual(set(w.readframes(w.getnframes())), {0})
    def test_reject_out_of_range(self):
        with tempfile.TemporaryDirectory() as d:
            for cuts in ((0.1,), (1.9,), (1.1, 0.8), (0.8, 0.8)):
                with self.assertRaises(ValueError):
                    make_cues(Path(d)/'bad.wav', 2.0, cuts, ())
    def test_reject_nan_and_long(self):
        with tempfile.TemporaryDirectory() as d:
            for duration in (float('nan'), 0.5, 91):
                with self.assertRaises(ValueError):
                    make_cues(Path(d)/'bad.wav', duration, (), ())
    def test_ten_genre_common_engine(self):
        cfg = json.loads((Path(__file__).resolve().parents[1] / 'genres.json').read_text(encoding='utf-8'))
        self.assertEqual(len(cfg['genres']), 10)
        self.assertEqual(len(set(cfg['genres'])), 10)
        self.assertFalse(cfg['defaults']['auto_post'])
        self.assertTrue(cfg['defaults']['require_human_review'])
        with tempfile.TemporaryDirectory() as d:
            for i, genre in enumerate(cfg['genres']):
                result = make_cues(Path(d)/f'genre_{i}.wav', 2.0, (0.7,), (1.0,))
                self.assertEqual(result['sample_rate'], 48000, genre)
    def test_parse(self):
        self.assertEqual(parse_times('0.7,1.4'), (0.7, 1.4))

if __name__ == '__main__':
    unittest.main()
