import hashlib
import importlib.util
import json
import pathlib
import unittest

P=pathlib.Path(__file__).resolve().parents[1]/'guided_tasks.py'
spec=importlib.util.spec_from_file_location('guided_tasks',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TestGuidedTasks(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(m.PALETTES),10)
    def test_stage_bounds(self):
        self.assertEqual(len(m.STAGES),3)
        self.assertTrue(all(b>a for a,b in m.STAGES))
        self.assertEqual(m.STAGES[0][0],3.0)
        self.assertLess(m.STAGES[-1][1],6.0)
    def test_caption_safe(self):self.assertLess(m.OVERLAY_HEIGHT,1400)
    def test_images_all_stages(self):
        for i in range(3):
            im=m.panel('ai',i)
            self.assertEqual(im.size,(1080,1270))
            self.assertGreater(len(set(im.resize((16,16)).getdata())),5)
    def test_distinct_stages(self):
        hashes=[hashlib.sha256(m.panel('ai',i).tobytes()).hexdigest() for i in range(3)]
        self.assertEqual(len(set(hashes)),3)
    def test_reject_invalid_genre(self):
        with self.assertRaises(ValueError):m.panel('unapproved',0)
    def test_reject_invalid_stage(self):
        with self.assertRaises(ValueError):m.panel('ai',4)
    def test_graph_has_three_gates(self):
        g=m.graph()
        self.assertEqual(g.count('overlay=x=0:y=0'),3)
        self.assertIn('lt(t,5.96)',g)
    def test_no_subtitle_edit(self):
        self.assertLess(m.OVERLAY_HEIGHT,1490)
    def test_policy_fail_closed(self):
        self.assertIn('NOT_APPROVED',m.POLICY)

if __name__=='__main__':unittest.main()
