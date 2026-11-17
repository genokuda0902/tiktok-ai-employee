import unittest
from pathlib import Path
import ast

class CaptionContract(unittest.TestCase):
    def test_timing(self):
        tree=ast.parse(Path(__file__).with_name('render.py').read_text(encoding='utf-8'))
        assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CAPTIONS' for t in n.targets))
        captions=ast.literal_eval(assignment.value)
        self.assertEqual(len(captions),4)
        self.assertEqual(captions[0][1],0)
        self.assertEqual(captions[-1][2],8)
        self.assertTrue(all(captions[i][2]==captions[i+1][1] for i in range(3)))
    def test_no_unapproved_publish(self):
        source=Path(__file__).with_name('render.py').read_text(encoding='utf-8')
        self.assertIn("'REVIEW_ONLY'",source)
        self.assertIn("'narration_verified':False",source)
if __name__=='__main__': unittest.main()
