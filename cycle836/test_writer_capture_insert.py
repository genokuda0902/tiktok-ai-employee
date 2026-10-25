import unittest
from pathlib import Path
from cycle836.writer_capture_insert import window, validate_manifest, build_command
from cycle833.focal_layout import GENRES, FRAMES

GOOD={'source_kind':'local_gui_capture','data_classification':'fictional',
      'contains_personal_data':False,'review_only':True,
      'publication_approved':False,'application':'LibreOffice Writer'}
class TestReviewCompositor(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES:
            self.assertEqual(window(g,6),(sum(FRAMES[:6]),sum(FRAMES[:7])))
    def test_all_eight_scenes(self):
        for i in range(8): self.assertEqual(window('ai_work',i)[1]-window('ai_work',i)[0],FRAMES[i])
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError): window('unknown',6)
    def test_reject_scene(self):
        with self.assertRaises(ValueError): window('ai_work',8)
    def test_safe_zone(self):
        with self.assertRaises(ValueError): window('ai_work',6,(62,390,1018,1510))
    def test_valid_fictional(self): validate_manifest(GOOD)
    def test_synthetic_fixture(self):
        validate_manifest({**GOOD,'source_kind':'synthetic_test_pattern','application':'synthetic_ffmpeg_fixture'})
    def test_reject_private(self):
        with self.assertRaises(ValueError): validate_manifest({**GOOD,'contains_personal_data':True})
    def test_reject_published(self):
        with self.assertRaises(ValueError): validate_manifest({**GOOD,'publication_approved':True})
    def test_reject_unknown_app(self):
        with self.assertRaises(ValueError): validate_manifest({**GOOD,'application':'browser'})
    def test_reject_missing_manifest(self):
        with self.assertRaises(ValueError): validate_manifest({})
    def test_reject_missing_files(self):
        with self.assertRaises(FileNotFoundError): build_command(Path('missing.mp4'),Path('missing2.mp4'),Path('out.mp4'),GOOD)
if __name__=='__main__':unittest.main()
