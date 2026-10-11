"""Zero-cost offline regression checks for cycle503 original ambient cue bed."""
import array
import math
import tempfile
import unittest
import wave
from pathlib import Path
from audio_bed import (SAMPLE_RATE, SECONDS, SCENE_CUTS, safety_check,
                       cue_signal, smooth_boundary, synthesize_pcm, write_wav)

class SafetyTests(unittest.TestCase):
    def test_review_only(self):
        safety_check('original_procedural', 'sfx_only')
    def test_unapproved_rights(self):
        for value in ('unknown', 'external_reference', 'confidential', ''):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safety_check(value, 'sfx_only')
    def test_unverified_narration(self):
        for value in ('japanese_verified', 'silent', 'unknown'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safety_check('original_procedural', value)
    def test_no_auto_post(self):
        with self.assertRaises(ValueError):
            safety_check('original_procedural', 'sfx_only', auto_post=True)
    def test_no_public_release(self):
        with self.assertRaises(ValueError):
            safety_check('original_procedural', 'sfx_only', public_release_approved=True)
    def test_no_private_data(self):
        with self.assertRaises(ValueError):
            safety_check('original_procedural', 'sfx_only', private_data=True)

class AudioTests(unittest.TestCase):
    def test_eight_scene_cues(self):
        self.assertEqual(len(SCENE_CUTS), 8)
    def test_cue_spacing(self):
        self.assertEqual(tuple(round(SCENE_CUTS[i+1] - SCENE_CUTS[i], 3)
            for i in range(7)), (2.5,) * 7)
    def test_cue_is_finite(self):
        for t in (0, .01, 2.5, 5.01, 19.99):
            self.assertTrue(math.isfinite(cue_signal(t)))
    def test_boundary_zero(self):
        self.assertEqual(smooth_boundary(0), 0)
        self.assertEqual(smooth_boundary(SECONDS), 0)
    def test_boundary_full_inside(self):
        self.assertEqual(smooth_boundary(2), 1)
    def test_short_pcm(self):
        samples = synthesize_pcm(4410)
        self.assertEqual(len(samples), 4410)
        self.assertEqual(samples[0], 0)
        self.assertGreater(max(samples), 0)
        self.assertLess(max(abs(x) for x in samples), 32767)
    def test_pcm_invalid(self):
        with self.assertRaises(ValueError):
            synthesize_pcm(0)
    def test_wav_header(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'audio.wav'
            write_wav(f, synthesize_pcm(4410))
            with wave.open(str(f)) as w:
                self.assertEqual(w.getframerate(), SAMPLE_RATE)
                self.assertEqual(w.getnchannels(), 1)
                self.assertEqual(w.getnframes(), 4410)
    def test_type_guard(self):
        with tempfile.TemporaryDirectory() as d, self.assertRaises(TypeError):
            write_wav(Path(d)/'x.wav', array.array('f', [0.1]))

if __name__ == '__main__':
    unittest.main()
