"""Synthetic-only tests; do not upload or commit source media."""
import importlib.util, pathlib, sys, unittest
import numpy as np
p=pathlib.Path(__file__).resolve().parent/'transition_earcon.py'
spec=importlib.util.spec_from_file_location('transition_earcon',p)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
class EarconTests(unittest.TestCase):
    def test_ten_distinct_genre_policies(self):
        self.assertEqual(len(m.GENRE_PRESETS),10)
        self.assertEqual(len(set(m.GENRE_PRESETS.values())),10)
    def test_synth_deterministic(self):
        self.assertTrue(np.array_equal(m.earcon(),m.earcon()))
    def test_short_nonmusical_sound(self):
        s=m.earcon();self.assertEqual(len(s),6720)
        self.assertLessEqual(float(np.max(np.abs(s))),10**(-27/20)+1e-9)
    def test_zero_outside_transition_window(self):
        x=np.zeros(2*m.SR)
        y,ev=m.add_earcons(x,[{'time_s':1,'scene':2,'visual_change_score':30}])
        self.assertEqual(len(ev),1)
        self.assertTrue(np.all(y[:m.SR]==0))
        self.assertTrue(np.all(y[m.SR+6720:]==0))
        self.assertGreater(np.max(abs(y[m.SR:m.SR+6720])),0)
    def test_voice_ducking(self):
        e=[{'time_s':1,'scene':2,'visual_change_score':30}]
        _,quiet=m.add_earcons(np.zeros(2*m.SR),e)
        _,loud=m.add_earcons(np.ones(2*m.SR)*.1,e)
        self.assertEqual(quiet[0]['cue_gain_db'],-2)
        self.assertEqual(loud[0]['cue_gain_db'],-9)
    def test_no_unreviewed_genre_render(self):
        for genre in set(m.GENRE_PRESETS)-m.REVIEWED_GENRES:
            with self.assertRaises(PermissionError):m.add_earcons(np.zeros(m.SR),[],genre)
    def test_unknown_genre_fails(self):
        with self.assertRaises(ValueError):m.add_earcons(np.zeros(m.SR),[],'not_real')
    def test_peak_guard(self):
        with self.assertRaises(ValueError):m.add_earcons(np.ones(2*m.SR)*.9,[{'time_s':1,'scene':2,'visual_change_score':30}])
if __name__=='__main__':unittest.main()
