import tempfile
import unittest
from pathlib import Path
import numpy as np
import sound_cue_engine as m

class CueEngineTests(unittest.TestCase):
    def test_ten_distinct_genre_policies(self):
        self.assertEqual(len(m.GENRE_CUE_POLICIES),10)
        self.assertEqual(len(set(m.GENRE_CUE_POLICIES.values())),10)
    def test_only_ai_work_reviewed(self):
        self.assertEqual(m.REVIEWED,{'ai_work'})
    def test_original_waveform_is_not_silent(self):
        x=m.synthesize();self.assertGreater(np.count_nonzero(x),100)
    def test_peak_bounded(self):
        self.assertLessEqual(float(np.max(np.abs(m.synthesize()))),m.MAX_CUE_PEAK+1e-6)
    def test_starts_ends_at_zero(self):
        p=m.cue_waveform(500,700,.15)
        self.assertAlmostEqual(float(p[0]),0,places=6)
        self.assertAlmostEqual(float(p[-1]),0,places=6)
    def test_all_cues_inside_runtime(self):
        self.assertTrue(all(0<=s<s+d<m.DURATION for _,s,_,_,d in m.EVENTS))
    def test_cues_do_not_overlap(self):
        self.assertTrue(all(m.EVENTS[i][1]+m.EVENTS[i][4]<m.EVENTS[i+1][1] for i in range(len(m.EVENTS)-1)))
    def test_cue_times_distinct(self):
        self.assertEqual(len({e[1] for e in m.EVENTS}),len(m.EVENTS))
    def test_outside_cue_windows_silent(self):
        x=m.synthesize();self.assertEqual(float(x[0]),0)
        self.assertEqual(float(x[int(3*48000)]),0)
    def test_stereo_pcm(self):
        import wave
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'cue.wav';m.write_wav(p,m.synthesize())
            with wave.open(str(p)) as f:
                self.assertEqual((f.getnchannels(),f.getframerate(),f.getsampwidth()),(2,48000,2))
    def test_reject_excess_gain(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):m.write_wav(Path(td)/'x.wav',np.ones(20,dtype=np.float32))
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):m.validate('/does/not/exist','unknown')
    def test_reject_unreviewed_genre(self):
        with self.assertRaises(ValueError):m.validate('/does/not/exist','health')
    def test_reject_missing_source(self):
        with self.assertRaises(ValueError):m.validate('/does/not/exist')
    def test_reject_publish_override(self):
        with self.assertRaises(ValueError):m.validate('/does/not/exist',publication_approved=True)
    def test_reject_review_only_override(self):
        with self.assertRaises(ValueError):m.validate('/does/not/exist',review_only=False)
    def test_sha_pin_rejects_wrong_media(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'source.mp4';p.write_bytes(b'fake')
            with self.assertRaises(ValueError):m.validate(p)
    def test_synth_is_deterministic(self):
        self.assertTrue(np.array_equal(m.synthesize(),m.synthesize()))
    def test_no_external_sound_assets(self):
        import inspect
        s=inspect.getsource(m.synthesize)+inspect.getsource(m.cue_waveform)
        self.assertNotIn('http',s);self.assertNotIn('requests',s)

if __name__=='__main__':unittest.main()
