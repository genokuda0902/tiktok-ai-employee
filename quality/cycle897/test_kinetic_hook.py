import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from kinetic_hook import *

class TestKineticHook(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_three_native_states(self):
        panels=[stage_panel(i,HookCopy()) for i in range(3)]
        self.assertTrue(all(p.size==CARD_SIZE for p in panels))
        self.assertEqual(len({p.tobytes() for p in panels}),3)
    def test_safe_card(self):
        self.assertEqual(stage_panel(1,HookCopy()).getpixel((939,0))[3],0)
        self.assertLess(CARD_ORIGIN[1]+CARD_SIZE[1],1450)
        self.assertGreater(RAIL_ORIGIN[1],1700)
    def test_crossfade(self):
        self.assertNotEqual(hook_frame(29,HookCopy()).tobytes(),hook_frame(33,HookCopy()).tobytes())
    def test_progress(self):
        self.assertEqual(rail_frame(0).size,(945,18))
        self.assertNotEqual(rail_frame(1).tobytes(),rail_frame(25).tobytes())
    def test_scene_boundaries(self):
        self.assertEqual([scene_index(x) for x in [0,3,6,9,12,15,18,22]],list(range(8)))
    def test_bad_copy_fails_closed(self):
        for bad in (HookCopy('保証'*10),HookCopy(example='http://example.com')):
            with self.assertRaises(ValueError):bad.validate()
    def test_out_of_range(self):
        with self.assertRaises(ValueError):rail_frame(691)
        with self.assertRaises(ValueError):stage_panel(3,HookCopy())

if __name__=='__main__':unittest.main()
