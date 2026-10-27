import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from native_document_reveal import DocumentSpec,render,SIZE
class NativeDocumentTests(unittest.TestCase):
    def setUp(self):self.spec=DocumentSpec('週次報告｜見本',(('成果','要点を整理'),('根拠','数字を明記'),('次の行動','期限を決める')))
    def test_dimensions_and_transparency(self):
        im=render(self.spec,0)
        self.assertEqual(im.size,SIZE);self.assertEqual(im.mode,'RGBA')
        self.assertEqual(im.getpixel((5,5))[3],0);self.assertEqual(im.getpixel((300,500))[3],255)
    def test_three_states_distinct(self):
        ims=[render(self.spec,i) for i in range(3)]
        self.assertNotEqual(ims[0].tobytes(),ims[1].tobytes())
        self.assertNotEqual(ims[1].tobytes(),ims[2].tobytes())
    def test_ten_genres(self):
        for name in ['AI・仕事効率化','営業','雑学','科学','歴史','料理','旅行','生活','金融教育','健康一般']:
            with self.subTest(name=name):self.assertEqual(render(DocumentSpec(name,((name,'短い説明'),)),0).size,SIZE)
    def test_rejects_overflow(self):
        with self.assertRaises(ValueError):render(DocumentSpec('x',(('label','a'*40),)),0)
    def test_rejects_empty(self):
        with self.assertRaises(ValueError):render(DocumentSpec('',(('x','y'),)),0)
    def test_rejects_out_of_range(self):
        with self.assertRaises(ValueError):render(self.spec,3)
    def test_deterministic(self):
        self.assertEqual(render(self.spec,0).tobytes(),render(self.spec,0).tobytes())
if __name__=='__main__':unittest.main()
