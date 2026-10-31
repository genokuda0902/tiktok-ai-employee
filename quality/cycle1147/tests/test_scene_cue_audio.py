import importlib.util,math,struct,tempfile,unittest,wave
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'code'/'scene_cue_audio.py'
spec=importlib.util.spec_from_file_location('scene_cue_audio',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class SceneCueTests(unittest.TestCase):
    def test_length(self):self.assertEqual(len(m.cue_samples()),7680)
    def test_repeatable(self):self.assertEqual(m.cue_samples(),m.cue_samples())
    def test_peak(self):self.assertAlmostEqual(max(abs(v) for v in m.cue_samples()),10**(-22/20),places=5)
    def test_endpoints(self):
        x=m.cue_samples();self.assertEqual(x[0],0);self.assertLess(abs(x[-1]),.0001)
    def test_speech_avoidance(self):
        pcm=[0]*96000
        for i in range(38400,51840):pcm[i]=12000
        x=m.quiet_placements(pcm,[1.0])[0]
        self.assertGreater(x['cue_start'],1.0)
        self.assertLessEqual(abs(x['offset_ms']),180)
    def test_silence_choice(self):
        pcm=[0]*96000
        x=m.quiet_placements(pcm,[1.0])[0]
        self.assertLess(x['speech_window_rms_dbfs'],-70)
    def test_wav(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'stem.wav'
            peak=m.write_stem(p,2.0,[{'cue_start':.5},{'cue_start':1.5}])
            with wave.open(str(p)) as f:
                self.assertEqual(f.getframerate(),48000)
                self.assertEqual(f.getnframes(),96000)
                raw=f.readframes(f.getnframes())
            self.assertGreater(max(abs(v) for v in struct.unpack('<'+'h'*(len(raw)//2),raw)),300)
            self.assertLess(peak,.1)
    def test_empty(self):self.assertEqual(m.quiet_placements([0]*48000,[]),[])
    def test_end_clamp(self):
        x=m.quiet_placements([0]*48000,[.9])[0]
        self.assertLessEqual(x['cue_start']+.16,1.001)

if __name__=='__main__':unittest.main()
