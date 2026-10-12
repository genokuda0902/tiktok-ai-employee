import unittest
import safe_stage_nav as nav

class StageNavTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(nav.GENRES), 10)
    def test_footer_geometry(self):
        nav.validate_geometry()
    def test_legacy_header_rejected(self):
        with self.assertRaises(ValueError):
            nav.validate_geometry((77,147,900,43))
    def test_stage_schedule(self):
        nav.validate_stages()
    def test_invalid_stage(self):
        with self.assertRaises(ValueError):
            nav.validate_stages(((2.5,5,'課題'),(4,10,'操作'),(10,15,'結果'),(15,17.5,'確認')))
    def test_filter_count(self):
        graph=nav.filtergraph()
        self.assertEqual(graph.count('drawtext='), 8)
        self.assertEqual(graph.count('drawbox='), 8)

if __name__=='__main__':
    unittest.main()
