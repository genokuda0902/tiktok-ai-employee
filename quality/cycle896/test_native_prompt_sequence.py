import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from native_prompt_sequence import PromptSpec,render,SIZE

GENRES=['AI時短','営業','雑学','科学','歴史','料理','旅行','生活','金融教育','健康一般']

class TestPromptSequence(unittest.TestCase):
    def setUp(self):
        self.spec=PromptSpec('目的と条件を3つに整理',(
            ('目的','上司への週次報告'),('条件','数字と根拠を入れる'),('形式','箇条書き3点')))
    def test_all_states_native(self):
        for i in range(3):
            self.assertEqual(render(self.spec,i).size,SIZE)
    def test_unique_states(self):
        self.assertEqual(len({render(self.spec,i).tobytes() for i in range(3)}),3)
    def test_caption_header_transparent(self):
        for i in range(3):
            im=render(self.spec,i)
            for xy in [(10,10),(500,250),(500,1320),(500,1510),(1000,1880)]:
                self.assertEqual(im.getpixel(xy)[3],0)
    def test_card_opaque(self):
        self.assertEqual(render(self.spec,0).getpixel((500,650))[3],255)
    def test_ten_genres(self):
        for genre in GENRES:
            s=PromptSpec(f'{genre}の指示を整理',(
                ('目的','成果を明確にする'),('条件','数字で説明する'),('形式','3点でまとめる')))
            self.assertEqual(render(s,2).size,SIZE)
    def test_invalid_field_count(self):
        with self.assertRaises(ValueError):
            render(PromptSpec('テスト',(('目的','入力'),)),0)
    def test_overlong_text_rejected(self):
        with self.assertRaises(ValueError):
            render(PromptSpec('テスト',(('目的','あ'*18),('条件','入力'),('形式','入力'))),0)
    def test_bad_active_rejected(self):
        with self.assertRaises(ValueError):
            render(self.spec,3)

if __name__=='__main__':
    unittest.main()
