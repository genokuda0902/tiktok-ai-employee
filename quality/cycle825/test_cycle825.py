import importlib.util,json,tempfile,unittest
from pathlib import Path
D=Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location(name,D/(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
img=load('image_scene825');qa=load('audit825')

class Test825(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(img.GENRES),10)
        for genre in img.GENRES:
            with tempfile.TemporaryDirectory() as td:
                p=Path(td)/'a.json'
                p.write_text(json.dumps({'origin':'procedural_original','review_allowed':True,
                    'private_data':False,'publication_approved':False}))
                self.assertEqual(img.validate_manifest(p,genre)['origin'],'procedural_original')
    def test_fail_closed(self):
        for item in ({'origin':'unknown','review_allowed':True,'private_data':False,'publication_approved':False},
                     {'origin':'procedural_original','review_allowed':False,'private_data':False,'publication_approved':False},
                     {'origin':'procedural_original','review_allowed':True,'private_data':True,'publication_approved':False}):
            with tempfile.TemporaryDirectory() as td:
                p=Path(td)/'a.json';p.write_text(json.dumps(item))
                with self.assertRaises(PermissionError):img.validate_manifest(p,'ai_work')
    def test_safe_box(self):
        x,y,w,h=img.SAFE_IMAGE_BOX
        self.assertLessEqual(y+h,1150)
        self.assertIn('overlay=',img.make_filter(6.47,2.98))
    def test_invalid_timing(self):
        with self.assertRaises(ValueError):img.make_filter(-1,3)
    def test_normalize_japanese(self):
        self.assertEqual(qa.normalize('ＡＩ で仕事を\n早く。'),'AIで仕事を早く。')
    def test_ass_parsing(self):
        row='Dialogue: 0,0:00:00.00,0:00:01.00,Caption,,0,0,0,,{\\c&H00FFFFFF&}まず、\\N{\\c&H00000000&}確認\\Nする。'
        self.assertEqual(qa.caption_rows(row)[0][2],'まず、確認する。')
    def test_semantic_mismatch_detected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'source').mkdir();(root/'output').mkdir()
            (root/'source/voice_timing.json').write_text(json.dumps({
                'sentences':[{'text':'正しい。','seconds':3}]*8}))
            rows=[]
            for i in range(24):
                s=i
                rows.append(f'Dialogue: 0,0:00:{s:02}.00,0:00:{s+1:02}.00,Caption,,0,0,0,,誤り\\Nだ\\Nよ。')
            (root/'output/captions817.ass').write_text('\n'.join(rows))
            with self.assertRaises(ValueError):qa.audit(root)
    def test_review_only(self):
        s=(D/'image_scene825.py').read_text()
        self.assertIn("'auto_post':False",s)
        self.assertNotIn('requests.post(',s)
if __name__=='__main__':unittest.main()
