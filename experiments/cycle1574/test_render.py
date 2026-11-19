import unittest
from render import scene_index,SCENES,FPS,DURATION
class TestTimeline(unittest.TestCase):
    def test_scene_start(self): self.assertEqual(scene_index(0),0)
    def test_scene_end(self): self.assertEqual(scene_index(DURATION),len(SCENES)-1)
    def test_frame_count(self): self.assertEqual(FPS*DURATION,240)
    def test_no_implicit_approval(self):
        import inspect,render
        self.assertIn("REVIEW ONLY",inspect.getsource(render.render))
if __name__=="__main__": unittest.main()
