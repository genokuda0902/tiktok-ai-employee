"""Cycle821: ten original Japanese storyboard scripts. No automatic publishing."""
from pathlib import Path
import json

GENRES = {
 "sales_business": ("営業・ビジネス","WORK SMARTER","仕事ができる人は、質問が違う。|まず、目指すゴールを確認する。|次に、今の数字を確かめる。|そして、理想との差を一つに絞る。|原因には、なぜを三回重ねる。|対策は、今日できる行動に変える。|結果を見て、また修正する。|小さな改善が、強いチームをつくる。"),
 "ai_work": ("AI仕事術","AI × WORK","AIで仕事を早くするなら、最初の一歩が大事。|まず、繰り返している作業を書き出す。|次に、完成形の見本を用意する。|指示は、目的と条件を具体的に伝える。|最初の出力は、必ず自分で確かめる。|違いがあれば、修正点を一つずつ伝える。|使える指示は、テンプレートに残す。|小さな時短を、毎日の習慣にしよう。"),
 "beauty": ("美容","BEAUTY ROUTINE","朝の身だしなみは、順番を決めると楽になる。|まず、肌の状態をやさしく確認する。|洗顔は、こすりすぎないことを意識する。|保湿は、自分の肌に合うものを選ぶ。|外出前は、日差しへの対策も忘れずに。|使うアイテムは、必要なものだけに絞る。|肌に合わなければ、無理に続けない。|続けやすいケアから、始めてみよう。"),
 "love_psychology": ("恋愛・心理","RELATIONSHIPS","会話が続く人には、共通する習慣がある。|まず、相手の話を最後まで聞く。|次に、気になったことを一つ質問する。|答えを急がず、相手の言葉を受け取る。|自分の気持ちも、短く素直に伝える。|意見が違っても、すぐに否定しない。|会話のあとに、感謝を言葉にする。|小さなやりとりが、信頼を育てていく。"),
 "money_saving": ("節約・家計","MONEY HABITS","お金の管理は、難しく考えなくていい。|まず、今月の支出を三つに分ける。|固定費と変動費を、見える形にする。|使っていない契約がないか確かめる。|買う前に、本当に必要かを考える。|無理な節約より、続けられる方法を選ぶ。|週に一度、支出を振り返る。|小さな見直しから、家計を整えよう。"),
 "career": ("キャリア","CAREER NOTES","仕事の成長は、振り返りから始まる。|まず、今できることを三つ書き出す。|次に、伸ばしたい力を一つ選ぶ。|目標は、今週の行動にまで小さくする。|わからないことは、早めに質問する。|学んだことは、実際の仕事で試す。|一週間後に、変化を確かめる。|昨日の自分より、一歩前へ進もう。"),
 "health_life": ("健康・生活","DAILY WELLNESS","毎日の調子は、小さな習慣で整えよう。|まず、起きる時間をできるだけ揃える。|朝は、光を浴びて体を目覚めさせる。|長く座ったら、少し体を動かす。|水分補給を、忘れない仕組みにする。|夜は、寝る前のスマホ時間を見直す。|無理のない範囲で、続け方を調整する。|できることから、一つ始めてみよう。"),
 "science": ("科学・雑学","CURIOUS SCIENCE","身近な不思議は、問いから始まる。|まず、気になる現象を観察する。|思い込みと、実際の事実を分けてみる。|理由を一つに決めつけず考える。|確かな資料で、説明を確かめる。|違う説明があれば、条件を比べる。|わかったことを、自分の言葉でまとめる。|小さな疑問が、学びを広げていく。"),
 "travel_food": ("旅行・グルメ","TRAVEL & FOOD","週末のお出かけは、余白があると楽しい。|まず、行きたい場所を一つ決める。|移動時間は、少し余裕を持って調べる。|食事の候補も、二つほど用意する。|混みそうな時間帯は、先に確認する。|予定を詰め込みすぎないようにする。|気になった景色や味を、記録に残す。|自分らしい旅の楽しみ方を見つけよう。"),
 "product_life": ("暮らし・商品","SMART LIVING","買い物で迷ったら、選ぶ基準を作ろう。|まず、何を解決したいのか決める。|次に、必要な機能を三つ書き出す。|見た目だけでなく、使いやすさも比べる。|置く場所と、お手入れの手間を考える。|予算を決めてから、候補を絞る。|買う前に、返品条件も確かめる。|長く使える一品を、じっくり選ぼう。")
}
GENRES={k:(name,tag,script.split("|")) for k,(name,tag,script) in GENRES.items()}

def validate():
 assert len(GENRES)==10
 for key,(name,tag,lines) in GENRES.items():
  assert name and tag and len(lines)==8 and len(set(lines))==8, key
  assert all(8<=len(line)<=33 and line.endswith("。") for line in lines),key
 return True

def write_catalog(path):
 validate()
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 data={k:{"genre_name":v[0],"visual_label":v[1],"scene_scripts":v[2],
 "voice_ready":k=="sales_business","approval":"HUMAN_REVIEW"} for k,v in GENRES.items()}
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
 return path

if __name__=="__main__":
 import argparse
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
 args=p.parse_args();print(write_catalog(args.output))
