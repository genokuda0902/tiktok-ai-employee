import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from weekly_zoom import GENRES, START_FRAME, FRAME_COUNT, WORK_BAND, SUBTITLE_TOP, stage_for_frame, safe_region, color_to_rgb

class SceneTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_scene_start(self): self.assertEqual(START_FRAME,87)
    def test_scene_length(self): self.assertEqual(FRAME_COUNT,87)
    def test_stage_start(self): self.assertEqual(stage_for_frame(0),0)
    def test_stage_second(self): self.assertEqual(stage_for_frame(29),1)
    def test_stage_third(self): self.assertEqual(stage_for_frame(58),2)
    def test_stage_end(self): self.assertEqual(stage_for_frame(86),2)
    def test_out_of_range(self):
        with self.assertRaises(ValueError):stage_for_frame(87)
    def test_safe_zone(self): self.assertTrue(safe_region())
    def test_caption_preserved(self): self.assertLess(WORK_BAND[3],SUBTITLE_TOP)
    def test_colors(self):
        for name,(color,task) in GENRES.items():
            with self.subTest(genre=name):
                self.assertEqual(len(color_to_rgb(color)),3)
                self.assertTrue(task)
    def test_no_external_media(self):
        s=Path(__file__).resolve().parents[1].joinpath('src/weekly_zoom.py').read_text()
        self.assertNotIn('requests.',s)
        self.assertNotIn('http://',s)
        self.assertNotIn('auto_post',s)
    def test_no_upload(self):
        s=Path(__file__).resolve().parents[1].joinpath('src/weekly_zoom.py').read_text()
        self.assertNotIn('upload_file(',s)
    def test_human_review_label(self):
        s=Path(__file__).resolve().parents[1].joinpath('src/weekly_zoom.py').read_text()
        self.assertIn('公開前に人が確認',s)
if __name__=='__main__': unittest.main()
