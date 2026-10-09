import unittest
from quality_contract import Scene, check_story

class TestProofCaption(unittest.TestCase):
    def test_missing_id(self):
        scenes = [Scene('HOOK',0,1,'hook'),Scene('BEFORE',1,3,'before'),Scene('TRANSFORM',3,5,'transform'),Scene('PROOF',5,8,'根拠を確認',('R1',)),Scene('RESULT',8,11,'result'),Scene('COMPARE',11,16,'compare'),Scene('CTA',16,20,'cta')]
        with self.assertRaises(ValueError):
            check_story(scenes,manifest={'rights':'SYNTHETIC_ORIGINAL','privacy':'NO_REAL_PERSONAL_DATA','publication':'NOT_APPROVED','auto_post':False})
