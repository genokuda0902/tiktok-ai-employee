import importlib.util
import pathlib
import unittest

SRC = pathlib.Path(__file__).resolve().parents[1] / 'src' / 'review_gate.py'
spec = importlib.util.spec_from_file_location('review_gate', SRC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ReviewGateTests(unittest.TestCase):
    def test_geometry(self):
        self.assertTrue(m.validate())
        self.assertEqual(m.END - m.START, 87)
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRES), 10)
        for genre in m.GENRES:
            self.assertEqual(m.make_overlay(0, genre).size, (1080, 1920))
    def test_fail_closed(self):
        self.assertIn('PUBLICATION_NOT_APPROVED', m.POLICY)
        self.assertNotIn('APPROVED', m.POLICY.split(' / ')[0])
    def test_caption_band_transparent(self):
        for stage in range(3):
            im = m.make_overlay(stage)
            self.assertEqual(im.getpixel((500, 1500))[3], 0)
            self.assertEqual(im.getpixel((500, 1900))[3], 0)
    def test_three_states_differ(self):
        images = [m.make_overlay(i) for i in range(3)]
        self.assertNotEqual(images[0].tobytes(), images[1].tobytes())
        self.assertNotEqual(images[1].tobytes(), images[2].tobytes())
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): m.make_overlay(3)
        with self.assertRaises(ValueError): m.make_overlay(0, 'other')
    def test_source_has_no_automation(self):
        src = SRC.read_text()
        self.assertNotIn('auto_post', src)
        self.assertNotIn('upload_video', src)
        self.assertNotIn('merge_pull_request', src)
    def test_checklist_not_fabricated(self):
        self.assertEqual(m.CHECKS, ('数字・根拠', '日付・固有名詞', '断定的な表現'))
        self.assertNotIn('確認済み', SRC.read_text())

if __name__ == '__main__': unittest.main()
