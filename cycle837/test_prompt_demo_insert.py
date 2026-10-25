import unittest
from pathlib import Path
from cycle837.prompt_demo_insert import PROMPTS, scene_window, check_manifest, compose
from cycle833.focal_layout import GENRES, FRAMES
GOOD={'source_kind':'locally_rendered_ui','data_classification':'fictional',
      'contains_personal_data':False,'review_only':True,
      'publication_approved':False,'service_connection':False}
class PromptDemoSafety(unittest.TestCase):
    def test_ten_genres_have_fictional_prompts(self):
        self.assertEqual(set(PROMPTS),set(GENRES));self.assertEqual(len(PROMPTS),10)
        for g,p in PROMPTS.items():
            self.assertIn('架空',p) if g!='ai_work' else self.assertIn('売上データ',p)
    def test_all_scene_windows(self):
        for g in GENRES:
            for i in range(8):
                s,e=scene_window(g,i)
                self.assertEqual(e-s,FRAMES[i]);self.assertEqual(s,sum(FRAMES[:i]))
    def test_exact_scene_four(self):self.assertEqual(scene_window('ai_work',3),(285,384))
    def test_safe_zone(self):
        with self.assertRaises(ValueError):scene_window('ai_work',3,(62,390,1018,1490))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):scene_window('unknown',3)
    def test_bad_scene(self):
        with self.assertRaises(ValueError):scene_window('ai_work',8)
    def test_boolean_scene_rejected(self):
        with self.assertRaises(ValueError):scene_window('ai_work',True)
    def test_valid_manifest(self):check_manifest(GOOD)
    def test_reject_personal_data(self):
        with self.assertRaises(ValueError):check_manifest({**GOOD,'contains_personal_data':True})
    def test_reject_service_connection(self):
        with self.assertRaises(ValueError):check_manifest({**GOOD,'service_connection':True})
    def test_reject_publication(self):
        with self.assertRaises(ValueError):check_manifest({**GOOD,'publication_approved':True})
    def test_reject_missing_provenance(self):
        with self.assertRaises(ValueError):check_manifest({})
    def test_reject_wrong_source(self):
        with self.assertRaises(ValueError):check_manifest({**GOOD,'source_kind':'real_chatgpt_capture'})
    def test_reject_missing_inputs(self):
        with self.assertRaises(FileNotFoundError):compose(Path('missing.mp4'),Path('missing2.mp4'),Path('out.mp4'),GOOD)
if __name__=='__main__':unittest.main()
