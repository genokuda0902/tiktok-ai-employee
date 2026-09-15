#!/usr/bin/env python3
import json
from pathlib import Path
shots=[
 {"t":[0,0.7],"type":"presenter","crop":"close","move":"push_in_1.18","overlay":"完成したExcel表を右奥に先見せ"},
 {"t":[0.7,2.2],"type":"result","crop":"macro","move":"snap_zoom","overlay":"バラバラ文章→表"},
 {"t":[2.2,3.6],"type":"pain","crop":"wide","move":"pan_down","overlay":"顧客メモ"},
 {"t":[3.6,5.5],"type":"presenter","crop":"medium","move":"dolly_left","overlay":"手入力まだやってる？"},
 {"t":[5.5,7.4],"type":"operation","crop":"full","move":"cursor_follow","overlay":"prompt typing"},
 {"t":[7.4,9.2],"type":"operation","crop":"full","move":"punch_in","overlay":"抽出項目"},
 {"t":[9.2,11.0],"type":"operation","crop":"full","move":"click_focus","overlay":"送信"},
 {"t":[11.0,13.0],"type":"operation","crop":"full","move":"micro_zoom","overlay":"生成中"},
 {"t":[13.0,15.0],"type":"operation","crop":"full","move":"row_reveal","overlay":"表1行目"},
 {"t":[15.0,17.5],"type":"operation","crop":"full","move":"copy_focus","overlay":"コピー"},
 {"t":[17.5,19.4],"type":"excel","crop":"full","move":"paste_hit","overlay":"貼り付け"},
 {"t":[19.4,21.5],"type":"excel","crop":"macro","move":"pull_out","overlay":"完成表"},
 {"t":[21.5,23.5],"type":"before_after","crop":"split","move":"wipe","overlay":"手入力→一括"},
 {"t":[23.5,25.2],"type":"presenter","crop":"close","move":"bounce_reaction","overlay":"これだけ"},
 {"t":[25.2,27.0],"type":"benefit","crop":"macro","move":"text_hit","overlay":"コピペ作業を減らす"},
 {"t":[27.0,29.2],"type":"presenter","crop":"medium","move":"push_in","overlay":"明日使うなら保存"},
 {"t":[29.2,31.2],"type":"next","crop":"card","move":"slide_up","overlay":"次回 営業メール10秒"},
 {"t":[31.2,33.0],"type":"brand","crop":"close","move":"slow_push","overlay":"AI時短ラボ"}
]
assert max(b-a for a,b in (x['t'] for x in shots)) <= 2.5
out=Path('output');out.mkdir(exist_ok=True)
(out/'v9_camera_plan.json').write_text(json.dumps({"shots":shots,"shot_count":len(shots),"avg_shot_seconds":33/len(shots)},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'v9 camera plan: {len(shots)} shots / {33/len(shots):.2f}s avg')
