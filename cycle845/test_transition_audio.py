import tempfile
import unittest
from pathlib import Path
import numpy as np
from cycle845.transition_audio import (CUT_FRAMES,FPS,GENRES,GATE,SAMPLE_RATE,
    overlay_cues,sound_cue,validate,sha256)

class TestAudioAccents(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_cuts_frame_exact(self):
        self.assertEqual(len(CUT_FRAMES),7)
        self.assertTrue(all(0<c<691 for c in CUT_FRAMES))
    def test_sfx_deterministic(self):
        self.assertTrue(np.array_equal(sound_cue(),sound_cue()))
    def test_sfx_not_silent(self):
        self.assertGreater(np.max(np.abs(sound_cue())),.01)
    def test_sfx_peak_guard(self):
        self.assertLessEqual(np.max(np.abs(sound_cue())),.025)
    def test_sfx_invalid_parameters(self):
        for kwargs in ({'peak':.2},{'pan':2},{'length':0}):
            with self.assertRaises(ValueError):sound_cue(**kwargs)
    def test_audio_unchanged_outside_cues(self):
        source=np.zeros((SAMPLE_RATE,2),np.float32)
        out,spans=overlay_cues(source,(10,20),peak=.012)
        mask=np.ones(len(source),bool)
        for a,b in spans:mask[a:b]=False
        self.assertTrue(np.array_equal(out[mask],source[mask]))
        self.assertTrue(np.any(out[~mask]!=0))
    def test_no_peak_clipping(self):
        src=np.zeros((SAMPLE_RATE,2),np.float32)
        out,_=overlay_cues(src,(10,),peak=.018)
        self.assertLess(np.max(np.abs(out)),.8913)
    def test_guard_loud_source(self):
        src=np.full((SAMPLE_RATE,2),.89,np.float32)
        with self.assertRaises(ValueError):overlay_cues(src,(10,),peak=.018)
    def test_bad_cut_order(self):
        with self.assertRaises(ValueError):overlay_cues(np.zeros((SAMPLE_RATE,2),np.float32),(20,10))
    def test_bad_audio_shape(self):
        with self.assertRaises(ValueError):overlay_cues(np.zeros(SAMPLE_RATE,np.float32),(10,))
    def test_fail_closed_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=Path(tmp)/'s.mp4';s.write_bytes(b'fictional-test')
            o=Path(tmp)/'o.mp4'
            m={**GATE,'source_sha256':sha256(s)}
            for genre in GENRES:validate(m,genre,s,o)
            for key in GATE:
                bad=m.copy();bad.pop(key)
                with self.assertRaises(ValueError):validate(bad,'ai_work',s,o)
            bad=m.copy();bad['source_sha256']='bad'
            with self.assertRaises(ValueError):validate(bad,'ai_work',s,o)
            with self.assertRaises(ValueError):validate(m,'unknown',s,o)
    def test_no_out_of_range_cue(self):
        with self.assertRaises(ValueError):overlay_cues(np.zeros((SAMPLE_RATE,2),np.float32),(100,))
if __name__=='__main__':unittest.main()
