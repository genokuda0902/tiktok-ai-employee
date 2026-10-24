"""Cycle820: original art and ten-genre theme tests. No posting or rights approval."""
import importlib.util, json, tempfile, unittest
from pathlib import Path
from PIL import Image
import make_art820 as art

class TestCycle820(unittest.TestCase):
    def test_ten_unique_palettes(self):
        self.assertEqual(len(art.PALETTES), 10)
        self.assertEqual(len(set(art.PALETTES.values())), 10)
    def test_eight_matching_narrations(self):
        self.assertEqual(len(art.SPEECH), 8)
        self.assertEqual(len(art.HEADS), 8)
        self.assertEqual(len(art.DURATIONS), 8)
        self.assertTrue(all(s.endswith('。') for s in art.SPEECH))
    def test_ten_genre_art_renders(self):
        with tempfile.TemporaryDirectory() as d:
            for name in art.PALETTES:
                path = Path(d) / (name + '.png')
                art.draw_scene(0, name, path)
                with Image.open(path) as im:
                    self.assertEqual(im.size, (1080,1920))
    def test_provenance_gate(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            art.create(root)
            m=json.loads((root/'source'/'asset_provenance.json').read_text())
            self.assertIn('no portraits',m['images'])
            self.assertFalse(m['publication_approved'])
    def test_unknown_genre_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                art.create(Path(d),'unknown')
    def test_narration_matches_existing_subtitle_renderer(self):
        p=Path(__file__).resolve().parents[1]/'cycle817'/'render817.py'
        spec=importlib.util.spec_from_file_location('render817',p)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        self.assertEqual([''.join(p) for p in module.PHRASES],art.SPEECH)

if __name__=='__main__':
    unittest.main()
