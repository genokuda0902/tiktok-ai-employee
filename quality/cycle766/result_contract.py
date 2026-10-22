"""cycle766: 10-genre result reveal contract, HUMAN_REVIEW only.
Full offline renderer is packaged with the generated MP4 for human review.
No TikTok posting or asset upload occurs in this module.
"""
from __future__ import annotations
FPS = 30
START_FRAME = 300
END_FRAME = 384
KEYFRAMES = 28
SOURCE_SHA256 = "11dd69cde63cdce6053b788e5eb6f768236dfcd4b9b80fd8700674eeab8ddd0d"
SALES = (120000, 150000, 200000, 180000)
GENRE_COLORS = {
 "AI・仕事効率化":"#42eadb","美容・身だしなみ":"#f4a3d6",
 "恋愛・心理":"#fb96a5","お金・節約":"#f5ca75",
 "営業・ビジネス":"#8bbcff","転職・キャリア":"#b1b5ff",
 "健康・生活改善":"#8bd9b0","雑学・科学":"#89e3f1",
 "旅行・グルメ":"#f4b58a","商品比較・暮らし":"#cdb5fa",
}

def ease(t: float) -> float:
 t=max(0.,min(1.,t))
 return t*t*(3-2*t)

def frame_to_stage(frame: int) -> int:
 if not isinstance(frame,int) or not START_FRAME<=frame<END_FRAME:
  raise ValueError("frame out of range")
 return (frame-START_FRAME)//3

def visible_values(frame: int) -> tuple[float,...]:
 t=frame_to_stage(frame)/(KEYFRAMES-1)
 return tuple(round(v/10000*ease((t*1.25-i*.15)/.70),3) for i,v in enumerate(SALES))

def validate_manifest(config: dict) -> None:
 if config.get("genre") not in GENRE_COLORS:raise ValueError("unsupported genre")
 if config.get("status")!="HUMAN_REVIEW":raise ValueError("approval gate")
 if config.get("post_policy")!="employee_manual_after_approval":raise ValueError("no auto posting")
 if config.get("asset_origin")!="original_synthetic_pillow":raise ValueError("rights gate")
 if config.get("synthetic_data") is not True:raise ValueError("data rights gate")
 if config.get("sales")!=list(SALES):raise ValueError("data mismatch")

def splice_filter() -> str:
 return (
  "[0:v]trim=start_frame=0:end_frame=300,setpts=PTS-STARTPTS[a];"
  "[1:v]setpts=PTS-STARTPTS[b];"
  "[0:v]trim=start_frame=384,setpts=PTS-STARTPTS[c];"
  "[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[out]"
 )
