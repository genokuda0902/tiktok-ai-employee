import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from prompt_component import render_art,GENRES,PARTS,W,H

class PromptTests(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES:self.assertEqual(render_art(1.1,g).size,(W,H))
    def test_three_distinct_elements(self):
        self.assertEqual(tuple(x[1] for x in PARTS),("目的","条件","形式"))
    def test_animation_changes_image(self):
        self.assertNotEqual(render_art(.05).tobytes(),render_art(2.4).tobytes())
    def test_invalid_genre_rejected(self):
        with self.assertRaises(ValueError):render_art(1,"unknown")
    def test_safe_region_height(self):
        self.assertEqual(H,803)
        self.assertLess(507+H,1365)
    def test_no_external_media(self):
        self.assertEqual(render_art(2.4).mode,"RGB")

if __name__=="__main__":unittest.main()
