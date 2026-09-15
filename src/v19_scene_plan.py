#!/usr/bin/env python3
import json
from pathlib import Path
scenes=[
(1,'hook','cinematic_robot',2.0,'これ、まだ手でやってるの？'),
(2,'pain','cinematic_human',2.0,'こんな悩みありませんか？'),
(3,'solution','cinematic_robot',2.0,'ChatGPT×Excelで一瞬'),
(4,'prompt','browser_proof',2.0,'やりたいことを自然な言葉で入力'),
(5,'generating','browser_proof',2.0,'分析・表・要点を自動生成'),
(6,'result','browser_proof',2.0,'結果が一瞬で見える'),
(7,'paste','spreadsheet_proof',2.0,'Excelへ貼り付け'),
(8,'chart','spreadsheet_proof',2.0,'グラフまで完成'),
(9,'before_after','cinematic_human',4.0,'面倒な作業がこう変わる'),
(10,'applications','motion_graphics',4.0,'要約・メール・可視化・アイデア・自動化'),
(11,'cta','cinematic_robot',4.0,'保存して明日使う'),
(12,'next','device_scene',2.0,'次回 ChatGPTでスライド資料'),
(13,'brand','cinematic_robot',2.0,'AI時短ラボ'),
(14,'message','cinematic_city',2.0,'AIで働き方はもっと自由になる'),
(15,'icons','motion_graphics',1.0,'時短・効率化・豊かな生活'),
(16,'finale','cinematic_robot',1.0,'また次の動画で')]
plan={'version':'v19','target':'reference-grade 16-scene TikTok','rule':'never stretch one proof screen into a whole video','resolution':'1080x1920','fps':30,'scenes':[{'id':i,'role':r,'engine':e,'duration':d,'message':m} for i,r,e,d,m in scenes], 'hard_reject':['single-screen-dominant','slide-deck-feel','low-resolution-crop','static-scene-over-2.2s','missing-cinematic-assets','missing-operation-proof']}
Path('output').mkdir(exist_ok=True)
Path('output/v19_scene_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(plan,ensure_ascii=False))
