"""Dependency-free CI policy tests for cycle912 (actual MP4 remains private)."""
from pathlib import Path
import ast
import unittest

SOURCE=Path(__file__).with_name('repetition_calendar.py')
TEXT=SOURCE.read_text(encoding='utf-8')
TREE=ast.parse(TEXT)

class Cycle912Policy(unittest.TestCase):
    def test_source_compiles(self):
        compile(TEXT,str(SOURCE),'exec')
    def test_ten_genres(self):
        node=next(n for n in ast.walk(TREE) if isinstance(n,ast.Assign)
                  and any(isinstance(t,ast.Name) and t.id=='GENRES' for t in n.targets))
        self.assertEqual(len(node.value.keys),10)
    def test_review_only(self):
        self.assertIn('review-only',TEXT)
        self.assertIn('no automatic posting',TEXT)
    def test_no_external_asset_url(self):
        for forbidden in ('http://','https://','@gmail.com','@yahoo.co.jp'):
            self.assertNotIn(forbidden,TEXT)
    def test_safe_area_and_frame_count(self):
        self.assertIn('SAFE_RIGHT=900',TEXT)
        self.assertIn('SAFE_BOTTOM=1460',TEXT)
        self.assertIn('W,H,FPS,FRAMES=1080,1160,30,87',TEXT)
    def test_no_post_or_upload_function(self):
        names={n.name for n in ast.walk(TREE) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
        self.assertFalse(names & {'post_video','publish','upload_to_tiktok','auto_post'})
    def test_visual_evidence_stages(self):
        self.assertIn("DAYS=('第1週','第2週','第3週')",TEXT)
        self.assertIn("idx-55",TEXT)
        self.assertIn("i*17",TEXT)
    def test_no_video_assets_committed(self):
        for p in SOURCE.parent.iterdir():
            self.assertNotIn(p.suffix.lower(),{'.mp4','.m4a','.aac','.wav'})
if __name__=='__main__':unittest.main()
