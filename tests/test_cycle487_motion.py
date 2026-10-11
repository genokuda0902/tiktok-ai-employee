import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'quality'/'cycle487'))
sys.path.insert(0,str(ROOT/'quality'/'cycle489'))
from motion import MotionShot,validate_motion,reveal_count,text_prefix,ALLOWED_GENRES
from contract import validate as validate_evidence
def shot(**k):return MotionShot('ai_productivity',0,2,8,caption='日本語',**k)
class GateTests(unittest.TestCase):
    def test_genres(self):self.assertEqual(len(ALLOWED_GENRES),10)
    def test_good(self):self.assertEqual(validate_motion([shot()],2)['publication'],'NOT_APPROVED')
    def test_stages(self):self.assertEqual(reveal_count(2.5),10)
    def test_prefix(self):self.assertEqual(text_prefix('=SUM(B2:B5)',1),'=SUM(B2:B5)')
    def test_auto_post(self):
        with self.assertRaises(ValueError):validate_motion([shot()],2,auto_post=True)
    def test_publication(self):
        with self.assertRaises(ValueError):validate_motion([shot()],2,publication='APPROVED')
    def test_unapproved_asset(self):
        with self.assertRaises(ValueError):validate_motion([MotionShot('ai_productivity',0,2,8,source='UNKNOWN',caption='x')],2)
    def test_missing_caption(self):
        with self.assertRaises(ValueError):validate_motion([MotionShot('ai_productivity',0,2,8)],2)
    def test_static(self):
        with self.assertRaises(ValueError):validate_motion([MotionShot('ai_productivity',0,2,1,caption='x')],2)
    def test_overlap(self):
        with self.assertRaises(ValueError):validate_motion([shot(),MotionShot('ai_productivity',1,3,8,caption='x')],3)
    def test_bad_duration(self):
        with self.assertRaises(ValueError):validate_motion([shot()],0)
    def test_reveal_invalid(self):
        with self.assertRaises(ValueError):reveal_count(0)
    def test_cycle489_evidence(self):self.assertTrue(validate_evidence())
    def test_cycle489_bad_total(self):
        with self.assertRaises(ValueError):validate_evidence((120,150,200,251))
    def test_cycle489_no_auto_post(self):
        with self.assertRaises(ValueError):validate_evidence(auto_post=True)
if __name__=='__main__':unittest.main()
