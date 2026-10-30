import tempfile
import unittest
from pathlib import Path
from pause_align import optimize,energy,MAX_SHIFT_SEC,run

class PauseAlignTests(unittest.TestCase):
    def test_energy_quiet(self):
        self.assertEqual(energy([0]*16000,16000,0.5),0)
    def test_energy_loud(self):
        self.assertGreater(energy([10000]*16000,16000,0.5),0.3)
    def test_pause_moves_boundary(self):
        sr=16000
        s=[12000]*int(sr*3)
        for i in range(int(sr*1.62),int(sr*1.85)): s[i]=0
        cues=[{'start':0,'end':1.5,'text':'日本語'},
              {'start':1.5,'end':3,'text':'字幕'}]
        a,r=optimize(cues,s,sr,3.0)
        self.assertNotEqual(a[0]['end'],1.5)
        self.assertLessEqual(abs(a[0]['end']-1.5),MAX_SHIFT_SEC)
        self.assertEqual(a[0]['end'],a[1]['start'])
        self.assertTrue(r[0]['pause_proxy_only'])
    def test_no_pause_does_not_shift(self):
        s=[12000]*48000
        cues=[{'start':0,'end':1.5,'text':'A'},
              {'start':1.5,'end':3,'text':'B'}]
        a,r=optimize(cues,s,16000,3.0)
        self.assertEqual(a[0]['end'],1.5)
        self.assertEqual(r[0]['delta_ms'],0)
    def test_captions_unchanged(self):
        s=[12000]*48000
        cues=[{'start':0,'end':1.5,'text':'日本語テスト'},
              {'start':1.5,'end':3,'text':'次の字幕'}]
        a,_=optimize(cues,s,16000,3.0)
        self.assertEqual([c['text'] for c in a],[c['text'] for c in cues])
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.mp4';p.write_bytes(b'x')
            m=Path(d)/'manifest.json';m.write_text('{}')
            with self.assertRaisesRegex(ValueError,'overwrite'):
                run(p,p,m,Path(d)/'work',synthetic=True)
    def test_hash_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.mp4';p.write_bytes(b'x')
            m=Path(d)/'manifest.json';m.write_text('{}')
            with self.assertRaisesRegex(ValueError,'SHA256'):
                run(p,Path(d)/'out.mp4',m,Path(d)/'work',expected_sha='wrong')
    def test_non_ai_genre_fail_closed(self):
        from cycle988.caption_mux import validate
        cues=[{'start':0,'end':3,'text':'日本語'}]
        for genre in ['finance','learning','health','travel','food',
                      'science','history','business','lifestyle']:
            with self.assertRaisesRegex(ValueError,'fail closed'):
                validate({'language':'ja','review_only':True,'cues':cues},3,genre)

if __name__=='__main__': unittest.main()
