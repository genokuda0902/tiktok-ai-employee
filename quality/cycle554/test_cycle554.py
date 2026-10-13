import unittest
from cycle554_renderer import GENRES, validate_proof, scene_frame, START, END

class TestProofScene(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:
            self.assertTrue(validate_proof([120,150,200,250],720,['1月','2月','3月','4月'],genre))
    def test_arithmetic_rejects_false_result(self):
        with self.assertRaises(ValueError):validate_proof([120,150],999,['1','2'],GENRES[0])
    def test_reject_negative(self):
        with self.assertRaises(ValueError):validate_proof([120,-150],-30,['1','2'],GENRES[0])
    def test_reject_float(self):
        with self.assertRaises(ValueError):validate_proof([120,1.2],121,['1','2'],GENRES[0])
    def test_reject_empty(self):
        with self.assertRaises(ValueError):validate_proof([],0,[],GENRES[0])
    def test_reject_labels(self):
        with self.assertRaises(ValueError):validate_proof([1,2],3,['only'],GENRES[0])
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):validate_proof([1],1,['one'],'UNKNOWN')
    def test_reject_scene_outside_video(self):
        with self.assertRaises(ValueError):validate_proof([1],1,['one'],GENRES[0],19,21)
    def test_scene_geometry(self):
        for t in [0,0.99,1,1.9,2.05,2.99]:self.assertEqual(scene_frame(t).size,(540,960))
    def test_reject_bad_frame_time(self):
        with self.assertRaises(ValueError):scene_frame(-.1)
    def test_timing(self):self.assertEqual((START,END),(9.0,12.0))

if __name__=='__main__':unittest.main()
