import unittest
import tempfile
from pathlib import Path
import numpy as np
from cycle845.transition_audio import SAMPLE_RATE,GENRES,GATE,sha256
from cycle846.voice_aware_sfx import adaptive_overlay,render

class TestAdaptiveSfx(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
    def test_ducks_when_voice_active(self):
        a=np.full((SAMPLE_RATE*2,2),.05,np.float32)
        _,d=adaptive_overlay(a,(30,))
        self.assertTrue(d[0]['speech_proxy_active'])
        self.assertEqual(d[0]['cue_gain'],.25)
    def test_full_gain_when_silent(self):
        a=np.zeros((SAMPLE_RATE*2,2),np.float32)
        _,d=adaptive_overlay(a,(30,))
        self.assertFalse(d[0]['speech_proxy_active'])
        self.assertEqual(d[0]['cue_gain'],1.)
    def test_centroid_aligned_to_cut(self):
        a=np.zeros((SAMPLE_RATE*2,2),np.float32)
        _,d=adaptive_overlay(a,(30,))
        self.assertGreater(d[0]['energy_centroid_offset_ms'],50)
        self.assertLess(d[0]['energy_centroid_offset_ms'],80)
        self.assertLess(d[0]['start_sample'],SAMPLE_RATE)
    def test_relative_reduction(self):
        s=np.zeros((SAMPLE_RATE*2,2),np.float32)
        loud=s.copy();loud[:]=.05
        out_s,_=adaptive_overlay(s,(30,))
        out_l,_=adaptive_overlay(loud,(30,))
        d0=out_s-s;d1=out_l-loud
        self.assertAlmostEqual(float(np.max(np.abs(d1)) / np.max(np.abs(d0))),.25,places=4)
    def test_outside_cues_bit_identical(self):
        a=np.zeros((SAMPLE_RATE*2,2),np.float32)
        out,d=adaptive_overlay(a,(30,))
        mask=np.ones(len(a),bool)
        mask[d[0]['start_sample']:d[0]['end_sample']]=False
        self.assertTrue(np.array_equal(out[mask],a[mask]))
    def test_deterministic(self):
        a=np.zeros((SAMPLE_RATE*2,2),np.float32)
        self.assertTrue(np.array_equal(adaptive_overlay(a,(30,))[0],adaptive_overlay(a,(30,))[0]))
    def test_rejects_invalid_input(self):
        a=np.zeros((SAMPLE_RATE,2),np.float32)
        for kw in ({'peak':.4},{'duck_gain':0},{'threshold':0}):
            with self.assertRaises(ValueError):adaptive_overlay(a,(10,),**kw)
        for cuts in ((-1,),(30,10),(200,),(10,10)):
            with self.assertRaises(ValueError):adaptive_overlay(a,cuts)
        with self.assertRaises(ValueError):adaptive_overlay(a[:,0],(10,))
    def test_rejects_peak_violation(self):
        a=np.full((SAMPLE_RATE,2),.89,np.float32)
        with self.assertRaises(ValueError):adaptive_overlay(a,(10,))
    def test_fail_closed_manifest(self):
        from cycle845.transition_audio import validate
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'s.mp4';p.write_bytes(b'test')
            o=Path(t)/'o.mp4'
            m={**GATE,'source_sha256':sha256(p)}
            for g in GENRES:validate(m,g,p,o)
            for key in GATE:
                bad=m.copy();bad.pop(key)
                with self.assertRaises(ValueError):validate(bad,'ai_work',p,o)
    def test_cue_is_quieter_under_speech(self):
        a=np.zeros((SAMPLE_RATE*2,2),np.float32)
        a[0:SAMPLE_RATE]=.08
        out,d=adaptive_overlay(a,(15,45))
        self.assertEqual([v['cue_gain'] for v in d],[.25,1.])
        self.assertTrue(np.max(np.abs(out-a))>0)

if __name__=='__main__':unittest.main()
