import unittest
from dataclasses import replace
from quality.cycle485.motion_contract import EvidenceScene, validate_scene, reveal_progress

S=EvidenceScene('売上グラフ',(120,150,200,250),('1月','2月','3月','4月'),720,12,14,(130,600,950,1470))

class TestContract(unittest.TestCase):
    def test_happy_path(self): self.assertEqual(validate_scene(S,20.166667)['verified_total'],720)
    def test_wrong_total(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,total=721),20.166667)
    def test_bad_rights(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,provenance='UNKNOWN'),20.166667)
    def test_publication(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,publication='APPROVED'),20.166667)
    def test_autopost(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,auto_post=True),20.166667)
    def test_empty(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,values=(),labels=()),20.166667)
    def test_mismatch_count(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,labels=('1月',)),20.166667)
    def test_bad_type(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,values=(120,150,200,250.0)),20.166667)
    def test_negative(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,values=(120,-150,200,250)),20.166667)
    def test_bad_timing(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,end=21),20.166667)
    def test_bad_bbox(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,bbox=(20,600,950,1470)),20.166667)
    def test_bad_lower_safearea(self):
        with self.assertRaises(ValueError): validate_scene(replace(S,bbox=(130,600,950,1760)),20.166667)
    def test_reveal_before(self): self.assertEqual(reveal_progress(0,1,1),0)
    def test_reveal_after(self): self.assertEqual(reveal_progress(3,1,1),1)
    def test_reveal_mid(self): self.assertAlmostEqual(reveal_progress(1.5,1,1),0.5)
    def test_reveal_nonfinite(self):
        with self.assertRaises(ValueError): reveal_progress(float('nan'),1,1)

if __name__ == '__main__': unittest.main()
