"""Synthetic-only tests. No private/user media in GitHub Actions."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import wave

SRC = Path(__file__).resolve().parents[1] / 'src' / 'transition_sound.py'
spec = importlib.util.spec_from_file_location('transition_sound', SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class SoundTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(mod.GENRE_PITCH), 10)
    def test_seven_scene_cuts(self):
        self.assertEqual(len(mod.SCENE_START_FRAMES), 7)
        self.assertEqual(tuple(sorted(mod.SCENE_START_FRAMES)), mod.SCENE_START_FRAMES)
    def test_review_policy(self):
        self.assertIn('PUBLICATION_NOT_APPROVED', mod.POLICY)
    def test_no_external_samples(self):
        text = SRC.read_text()
        self.assertNotIn('requests.get(', text)
        self.assertNotIn('upload_file(', text)
        self.assertNotIn('tiktok.post(', text)
    def test_gain_speech_ducking(self):
        self.assertLess(mod.cue_gain(0.1), mod.cue_gain(0.001))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):
            mod.synthesize_sfx([], 'not_a_genre')
    def test_determinism(self):
        voice = [0.0] * (mod.SAMPLE_RATE // 10)
        a, info_a = mod.synthesize_sfx(voice)
        b, info_b = mod.synthesize_sfx(voice)
        self.assertEqual(a.tobytes(), b.tobytes())
        self.assertEqual(info_a, info_b)
    def test_sfx_not_clipping(self):
        sfx, _ = mod.synthesize_sfx([])
        self.assertLess(max(abs(x) for x in sfx), 0.05)
    def test_sha_guard(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'test.mp4'
            p.write_bytes(b'test')
            with self.assertRaisesRegex(RuntimeError, 'SOURCE_SHA_MISMATCH'):
                mod.render(p, Path(d)/'out.mp4', Path(d)/'sfx.wav', expected_source_sha='wrong')
    def test_silence_between_cues(self):
        sfx, _ = mod.synthesize_sfx([])
        self.assertEqual(sfx[mod.SAMPLE_RATE], 0.0)
        self.assertEqual(sfx[int(4.5 * mod.SAMPLE_RATE)], 0.0)
    def test_cue_timing(self):
        sfx, cues = mod.synthesize_sfx([])
        self.assertEqual([x['frame'] for x in cues], list(mod.SCENE_START_FRAMES))
        self.assertTrue(all(0 < x['time_s'] < mod.DURATION for x in cues))
    def test_wav_format(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'test.wav'
            mod.write_wav(p, [0.0] * 100)
            with wave.open(str(p), 'rb') as f:
                self.assertEqual((f.getnchannels(), f.getframerate(), f.getsampwidth()), (1, 48000, 2))

if __name__ == '__main__':
    unittest.main()
