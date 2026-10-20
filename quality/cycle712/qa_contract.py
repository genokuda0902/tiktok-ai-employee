"""Cycle712 reusable ten-genre review-only QA contract (no approval implied)."""
from dataclasses import dataclass

GENRES=("AI仕事効率化","AI学習","AI副業","AIビジネス","AIニュース","AI生活","AIクリエイティブ","AIツール","AIプログラミング","AIマーケティング")
W,H,FPS=1080,1920,30
DURATION=24
VALUES=(120000,150000,200000,180000)
MONTHS=("1月","2月","3月","4月")
CAPTIONS=(
 "その売上集計、どうしてる？","まず元データを確認","AIに集計とグラフを指示","結果はそのまま使わない",
 "3月が最高の20万円","合計65万円を検算","AIで下書き、人が確認","手順を保存して試そう",
)
SPEAK=(
 "売上データの集計、まだ手作業ですか？","最初に、元の数字を確認します。",
 "エーアイに、月別のグラフを作ってと指示します。","ただし、出てきた結果をそのまま使わないでください。",
 "この例では、三月が二十万円で最高です。","合計は六十五万円。元データで検算します。",
 "エーアイが下書きして、人が確認する流れです。","手順を保存して、架空データで試してみてください。",
)
@dataclass(frozen=True)
class Approval:
 assets_approved:bool=False
 privacy_checked:bool=False
 voice_present:bool=False
 caption_voice_synced:bool=False
 human_reviewed:bool=False
 employee_approved:bool=False

def publishable(approval:Approval)->bool:
 return all(vars(approval).values())

def verify_story(values=VALUES,captions=CAPTIONS,genres=GENRES):
 if len(genres)!=10 or len(set(genres))!=10:raise ValueError("10 genre templates required")
 if len(values)!=4 or any(type(x) is not int or x<0 for x in values):raise ValueError("Invalid synthetic values")
 if sum(values)!=650000 or max(values)!=200000 or values.index(max(values))!=2:raise ValueError("Incorrect numeric proof")
 if len(captions)!=8 or any(len(s)>28 or len(s)==0 for s in captions):raise ValueError("Unsafe caption length")
 return True

def caption_safe(y1,y2):
 if y1<192 or y2>1536 or y2<=y1:raise ValueError("Caption overlaps UI unsafe region")
 return True

def make_srt(captions=CAPTIONS,seconds=3):
 def ts(n):
  h=int(n//3600);m=int(n//60)%60;s=int(n)%60;ms=int(round((n%1)*1000))
  return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
 return "\n".join(f"{i+1}\n{ts(i*seconds)} --> {ts((i+1)*seconds)}\n{cap}\n" for i,cap in enumerate(captions))
