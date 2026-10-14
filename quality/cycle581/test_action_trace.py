"""10-genre action cue and safety regression tests; no external services."""
import unittest
from PIL import Image
from action_trace import GENRES,SIZE,FPS,DEFAULT,ActionTrace,stage_at,frame
class ActionTraceTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES: self.assertTrue(ActionTrace(g,'テスト').validate())
    def test_unknown_genre_fails(self):
        with self.assertRaises(ValueError): ActionTrace('other','テスト').validate()
    def test_empty_message_fails(self):
        with self.assertRaises(ValueError): ActionTrace('beauty','').validate()
    def test_long_message_fails(self):
        with self.assertRaises(ValueError): ActionTrace('beauty','あ'*55).validate()
    def test_time_order_fails(self):
        with self.assertRaises(ValueError): ActionTrace('beauty','a',(0,2.5,1.5,3)).validate()
    def test_stage_transitions(self):
        self.assertEqual([stage_at(DEFAULT,t) for t in (0,1.84,1.85,2.39,2.4,2.99)],
                         ['input','input','submit','submit','ack','ack'])
    def test_invalid_time_fails(self):
        with self.assertRaises(ValueError): stage_at(DEFAULT,3.0)
    def test_frame_is_safe_zone_preserving(self):
        base=Image.new('RGB',SIZE,'#051122'); changed=frame(base,DEFAULT,80)
        self.assertNotEqual(changed.getpixel((800,1530)),base.getpixel((800,1530)))
        self.assertEqual(changed.getpixel((500,1700)),base.getpixel((500,1700)))
    def test_frame_bounds(self):
        with self.assertRaises(ValueError): frame(Image.new('RGB',(640,480)),DEFAULT,1)
        with self.assertRaises(ValueError): frame(Image.new('RGB',SIZE),DEFAULT,90)
    def test_duration(self): self.assertEqual(FPS*3,90)
if __name__=='__main__': unittest.main()
