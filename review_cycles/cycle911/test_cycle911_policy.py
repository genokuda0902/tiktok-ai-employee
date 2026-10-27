"""Dependency-free CI checks; actual MP4 is verified locally, not by this CI."""
import ast
import unittest
from pathlib import Path

SOURCE=Path(__file__).with_name('safe_cta.py')
TEXT=SOURCE.read_text(encoding='utf-8')
TREE=ast.parse(TEXT)
VALUES={}
for node in TREE.body:
    if not isinstance(node,ast.Assign) or len(node.targets)!=1: continue
    try: val=ast.literal_eval(node.value)
    except (ValueError,TypeError): continue
    target=node.targets[0]
    if isinstance(target,ast.Name): VALUES[target.id]=val
    elif isinstance(target,ast.Tuple) and isinstance(val,tuple):
        for name,item in zip(target.elts,val):
            if isinstance(name,ast.Name): VALUES[name.id]=item

class ReviewOnlyPolicy(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(VALUES['PALETTES']),10)
    def test_three_actions(self):
        self.assertEqual(len(VALUES['STEPS']),3)
    def test_right_ui_safe(self):
        self.assertLessEqual(VALUES['SAFE_RIGHT'],900)
    def test_bottom_caption_safe(self):
        self.assertLessEqual(VALUES['VIDEO_Y']+VALUES['H'],VALUES['SAFE_BOTTOM'])
    def test_1080_wide(self):
        self.assertEqual(VALUES['W'],1080)
    def test_82_frames(self):
        self.assertEqual(VALUES['FRAMES'],82)
    def test_no_posting(self):
        self.assertNotIn('requests.post(',TEXT)
        self.assertNotIn('tiktok_api',TEXT)
    def test_no_false_claims(self):
        self.assertIn('架空の説明用画面',TEXT)
        self.assertIn('社員確認・手動投稿のみ',TEXT)
    def test_all_steps_visible(self):
        self.assertIn('for i,(title,detail) in enumerate(STEPS):',TEXT)
        self.assertIn('im=base_image().copy()',TEXT)
    def test_font_and_bbox_check(self):
        self.assertIn('text_bbox(title,43,True)',TEXT)
        self.assertIn('validate_layout()',TEXT)

if __name__=='__main__':unittest.main()
