import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'source' / 'proof_focus.py'
spec = importlib.util.spec_from_file_location('proof_focus', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProofFocusTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRES), 10)
    def test_each_genre_has_two_safe_focuses(self):
        for genre in m.GENRES:
            with self.subTest(genre=genre):
                graph = m.filter_graph(genre)
                self.assertEqual(graph.count('w=480:h=144'), 2)
                self.assertEqual(graph.count('y=317:w=832'), 2)
                self.assertIn('between(t,5.950,7.200)', graph)
                self.assertIn('between(t,7.200,8.550)', graph)
    def test_caption_safe(self):
        graph = m.filter_graph('ai_work')
        self.assertNotIn('y=1490', graph)
        self.assertNotIn('y=1520', graph)
        self.assertIn('y=1303', graph)
    def test_real_data_label(self):
        graph = m.filter_graph('ai_work')
        self.assertIn('営業A  46', graph)
        self.assertIn('営業B  29', graph)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):
            m.filter_graph('unknown')
    def test_invalid_timing(self):
        with self.assertRaises(ValueError):
            m.filter_graph('ai_work', 8, 7, 6)
    def test_text_injection(self):
        with self.assertRaises(ValueError):
            m.safe_text('a:bad')
    def test_review_gate(self):
        with self.assertRaises(ValueError):
            m.render('missing', 'out', 'report', 'ai_work', '0' * 64)
    def test_missing_source(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                m.render(Path(d)/'missing', Path(d)/'out', Path(d)/'report', 'ai_work', '0'*64, True)
    def test_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'source'; path.write_text('placeholder')
            with self.assertRaises(ValueError):
                m.render(path, path, Path(d)/'report', 'ai_work', '0'*64, True)

if __name__ == '__main__':
    unittest.main()
