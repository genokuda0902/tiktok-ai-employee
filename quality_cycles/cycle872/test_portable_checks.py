import unittest
from portable_checks import *

class Cycle872Tests(unittest.TestCase):
    def test_ten_exact_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(set(GENRES.values()),{"AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネ","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし"} - {"営業・ビジネ"} | {"営業・ビジネス"})
    def test_all_genres_safe(self):
        for genre in GENRES: self.assertTrue(check_layout(genre=genre))
    def test_bad_genre(self):
        with self.assertRaises(ValueError): check_layout(genre="unknown")
    def test_photo_safe(self): self.assertTrue(check_layout())
    def test_photo_no_title_overlap(self):
        self.assertTrue(all(not Rect(*box).intersects(Rect(*TITLE)) for box in PORTRAITS.values()))
    def test_ui_crop(self):
        with self.assertRaises(ValueError): check_layout(crop=(100,300,870,1050))
    def test_ui_bounds(self):
        with self.assertRaises(ValueError): check_layout(crop=(-10,145,1080,1145))
    def test_caption_safe(self):
        with self.assertRaises(ValueError): check_layout(dest=(35,440,1045,1510))
    def test_stretch_rejected(self):
        with self.assertRaises(ValueError): check_layout(dest=(35,440,1045,1100))
    def test_eight_scenes(self): self.assertTrue(check_scenes())
    def test_scene_gap(self):
        s=list(SCENES);s[2]=(6,8.45)
        with self.assertRaises(ValueError): check_scenes(s)
    def test_frame_count(self): self.assertEqual(round(DURATION*FPS),691)
    def test_caption_count(self):
        b=[{"start":i*.9,"end":i*.9+.8,"text":"字幕"} for i in range(24)]
        self.assertTrue(check_captions(b))
    def test_caption_overlap(self):
        b=[{"start":i*.9,"end":i*.9+.8,"text":"字幕"} for i in range(24)]
        b[1]["start"]=.5
        with self.assertRaises(ValueError): check_captions(b)
    def test_probe(self):
        probe={"streams":[{"codec_type":"video","codec_name":"h264","width":1080,"height":1920,"r_frame_rate":"30/1","nb_frames":"691"},{"codec_type":"audio","codec_name":"aac","sample_rate":"48000"}],"format":{"duration":"23.033333"}}
        self.assertTrue(check_media_probe(probe))
if __name__=="__main__": unittest.main()
