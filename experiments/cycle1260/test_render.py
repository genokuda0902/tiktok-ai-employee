import unittest
from pathlib import Path
import ast
SOURCE=Path(__file__).with_name('render.py')
class RenderContract(unittest.TestCase):
    def test_three_scenes(self):
        tree=ast.parse(SOURCE.read_text())
        scenes=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SCENES' for t in n.targets))
        self.assertEqual(len(ast.literal_eval(scenes)),3)
    def test_review_only_and_no_upload(self):
        source=SOURCE.read_text()
        self.assertIn('HUMAN REVIEW ONLY',source)
        self.assertNotIn('tiktok.com/upload',source)
if __name__=='__main__':unittest.main()
