import unittest
from dataclasses import replace
from quality.cycle486.render_cycle486 import validate_plan, SCENES, VALUES, TOTAL, draw_scene

class TestCycle486(unittest.TestCase):
    def test_valid(self): self.assertTrue(validate_plan())
    def test_sum(self): self.assertEqual(sum(VALUES),720)
    def test_wrong_sum(self):
        with self.assertRaises(ValueError): validate_plan(total=721)
    def test_negative(self):
        with self.assertRaises(ValueError): validate_plan(values=(120,-150,200,250),total=420)
    def test_float(self):
        with self.assertRaises(ValueError): validate_plan(values=(120,150.0,200,250))
    def test_rights(self):
        with self.assertRaises(ValueError): validate_plan(rights='UNKNOWN')
    def test_publication(self):
        with self.assertRaises(ValueError): validate_plan(publication='APPROVED')
    def test_autopost(self):
        with self.assertRaises(ValueError): validate_plan(auto_post=True)
    def test_overlap(self):
        with self.assertRaises(ValueError): validate_plan(scenes=(('a',1,3),('b',2,4)))
    def test_duplicate(self):
        with self.assertRaises(ValueError): validate_plan(scenes=(('a',1,2),('a',3,4)))
    def test_out_of_range(self):
        with self.assertRaises(ValueError): validate_plan(scenes=(('a',20,21),))
    def test_empty(self):
        with self.assertRaises(ValueError): validate_plan(values=(),total=0)
    def test_scene_count(self): self.assertEqual(len(SCENES),7)
    def test_render_all(self):
        for i,(kind,_,_) in enumerate(SCENES,1):
            self.assertEqual(draw_scene(kind,i).size,(1080,1920))
if __name__=='__main__': unittest.main()
