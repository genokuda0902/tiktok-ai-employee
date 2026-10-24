import json
import math
import tempfile
import unittest
from pathlib import Path
from tighten_pacing import (FPS,RATE,HOP,EXPECTED_GENRES,original_frames,
                            last_active_seconds,keep_frames,load_manifest,filter_graph)

class PacingTests(unittest.TestCase):
    def test_ten_genres_contract(self):
        self.assertEqual(len(EXPECTED_GENRES),10)
    def test_original_frame_boundaries_have_no_accumulated_drift(self):
        times=[3.355,3.085,3.025,3.285,3.265,3.36,2.97,3.495]
        self.assertEqual(sum(original_frames(times)),round(sum(times)*FPS))
    def test_rms_detects_end_of_voice(self):
        x=[0]*(RATE//2)+[9000]*(RATE//2)+[0]*(RATE//2)
        self.assertAlmostEqual(last_active_seconds(x),1.0,delta=HOP/RATE)
    def test_silent_scene_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'No audible'):
            last_active_seconds([0]*RATE)
    def test_max_trim_and_speech_tail(self):
        n=original_frames([3.355])[0]
        k=keep_frames(3.355,2.88,n)
        self.assertGreaterEqual(k/FPS,2.88+0.22)
        self.assertLessEqual(n-k,math.ceil(0.30*FPS))
    def test_late_speech_does_not_cut(self):
        n=original_frames([3.0])[0]
        self.assertEqual(keep_frames(3.0,2.95,n),n)
    def test_bad_activity_fails_closed(self):
        with self.assertRaises(ValueError):keep_frames(3.0,3.2,90)
    def test_manifest_rejects_missing_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'timing.json'
            p.write_text(json.dumps({'genre':'sales_business','sentences':[{'scene':1,'text':'OK','seconds':3.0}]}))
            with self.assertRaises(ValueError):load_manifest(p)
    def test_manifest_rejects_wrong_scene_number(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'timing.json'
            p.write_text(json.dumps({'genre':'sales_business','voice_engine':'Open JTalk','sentences':[{'scene':2,'text':'OK','seconds':3.0}]}))
            with self.assertRaises(ValueError):load_manifest(p)
    def test_ffmpeg_graph_preserves_both_tracks(self):
        x=[{'source_start_frame':0,'output_frames':70,'audio_start':0.0},
           {'source_start_frame':90,'output_frames':75,'audio_start':3.0}]
        g=filter_graph(x)
        self.assertIn('concat=n=2:v=1:a=1',g)
        self.assertIn('trim=start_frame=90:end_frame=165',g)
        self.assertIn('atrim=start=3.000000',g)

if __name__=='__main__':unittest.main()
