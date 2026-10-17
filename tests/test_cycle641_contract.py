"""Zero-budget offline tests for cycle641."""
import importlib.util
import sys
import unittest
from pathlib import Path
source=Path(__file__).resolve().parents[1]/"quality"/"cycle641"/"visual_contract.py"
spec=importlib.util.spec_from_file_location("cycle641_contract",source)
m=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=m
spec.loader.exec_module(m)
class ContractTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(m.GENRES),10)
        self.assertEqual(len(set(m.GENRES)),10)
    def test_timeline(self):
        self.assertEqual((m.WIDTH,m.HEIGHT,m.FPS,m.FRAME_COUNT,m.SCENES),(1080,1920,30,600,8))
        self.assertEqual(m.scene_for_frame(0),0)
        self.assertEqual(m.scene_for_frame(599),7)
    def test_reject_bad_frame(self):
        for x in (-1,600,2.3,True):
            with self.assertRaises(ValueError):m.scene_for_frame(x)
    def test_gate(self):
        x=m.ReviewContract(asset_sha256="a"*64)
        self.assertTrue(m.validate(x))
        for k,v in [("auto_post",True),("publication","APPROVED"),("quality","APPROVED"),("rights","PUBLIC"),("narration","PRESENT"),("asset_sha256","bad")]:
            with self.assertRaises(ValueError):m.validate(m.ReviewContract(**{**x.__dict__,k:v}))
    def test_math(self):
        self.assertTrue(m.numeric_proof())
if __name__=="__main__":unittest.main()
