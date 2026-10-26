import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'tools'))
from cycle862_demo import BOUNDARIES,STEPS,GENRE_ACCENTS,frame_to_scene,typed_length,draw_frame
class TestCycle862Demo(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRE_ACCENTS),10)
    def test_eight_scenes(self): self.assertEqual(len(STEPS),8)
    def test_boundaries(self):
        self.assertEqual(BOUNDARIES[0],0);self.assertEqual(BOUNDARIES[-1],691)
        self.assertTrue(all(b>a for a,b in zip(BOUNDARIES,BOUNDARIES[1:])))
    def test_scene_transitions(self):
        for i in range(8):self.assertEqual(frame_to_scene(BOUNDARIES[i]/30),i)
    def test_final_frame(self):self.assertEqual(frame_to_scene(690/30),7)
    def test_text_typing(self):
        self.assertEqual(typed_length('あいうえお',0),0)
        self.assertEqual(typed_length('あいうえお',1),5)
    def test_render_dimensions(self):self.assertEqual(draw_frame(10).size,(900,420))
    def test_ten_genres_render(self):
        for genre in GENRE_ACCENTS:self.assertEqual(draw_frame(8.5,genre).mode,'RGBA')
    def test_unsupported_genre(self):
        with self.assertRaises(ValueError):draw_frame(2,'bad')
if __name__=='__main__':unittest.main()
