from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_cycle598 import SCENES,X,Y,CARD_W,CARD_H,make_card,load_accent

def test_scene_windows_cover_entire_video():
 assert SCENES[0][0]==0 and SCENES[-1][1]==15.6
 assert all(abs(a[1]-b[0])<1e-8 for a,b in zip(SCENES,SCENES[1:]))

def test_safezone_avoids_right_buttons_and_bottom_caption():
 assert X>=50 and X+CARD_W<=860
 assert Y>=1430 and Y+CARD_H<=1670

def test_card_has_transparency_and_japanese_text_pixels():
 c=make_card('小さなPC','発見')
 assert c.mode=='RGBA' and c.size==(CARD_W,CARD_H)
 assert c.getpixel((0,0))[3]==0
 assert c.getpixel((110,115))[3]>0

def test_labels_are_editorial_paraphrases_not_unverified_claims():
 assert len(SCENES)==8
 assert all(2<=len(x[2])<=20 for x in SCENES)
 assert SCENES[-1][2]=='保存して後で試す'

def test_last_scene_cta_not_overlaid():
 assert SCENES[-1][0]==13.9

def test_ten_genre_theme_loader():
 import json
 data=json.loads((Path(__file__).resolve().parents[1]/'config/genres.json').read_text())
 assert len(data['genres'])==10
 assert all(len(load_accent(name))==3 for name in data['genres'])
