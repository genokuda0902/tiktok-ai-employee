#!/usr/bin/env python3
import json
from pathlib import Path

# v19 retention-first timeline. No fixed next-episode preview: series teasers are optional Director decisions.
scenes=[
(1,'character','hook','premium_robot',2.0,'これ、まだ手でやってるの？'),
(2,'human','pain','cinematic_human',2.0,'こんな悩みありませんか？'),
(3,'character','solution','premium_robot',2.0,'ChatGPT×Excelで一瞬'),
(4,'browser_proof','prompt','browser_motion',2.0,'やりたいことを自然な言葉で入力'),
(5,'browser_proof','generating','browser_motion',2.0,'分析・表・要点を自動生成'),
(6,'browser_proof','result','browser_motion',2.0,'結果が一瞬で見える'),
(7,'spreadsheet_proof','paste','spreadsheet_motion',2.0,'Excelへ貼り付け'),
(8,'spreadsheet_proof','chart','spreadsheet_motion',2.0,'グラフまで完成'),
(9,'before_after','transformation','cinematic_human',4.0,'面倒な作業がこう変わる'),
(10,'motion_graphics','applications','motion_graphics',3.0,'要約・メール・可視化・アイデア・自動化'),
(11,'cta','save','premium_robot',3.0,'保存して明日使う'),
(12,'human','freedom','cinematic_city',2.0,'浮いた時間をもっと大切なことに'),
(13,'character','brand','premium_robot',2.0,'AI時短ラボ'),
(14,'motion_graphics','return_reason','motion_graphics',2.0,'毎日1つ仕事がラクになる'),
(15,'character','finale','premium_robot',1.0,'また使えるAI仕事術を')]

plan={
 'version':'v19',
 'target':'premium human-edited TikTok / high-quality video generation app output',
 'rule':'proof-first, no fixed next-preview, never stretch one proof screen into a whole video',
 'resolution':'1080x1920','fps':30,
 'scenes':[{'id':i,'type':t,'role':r,'engine':e,'duration':d,'message':m} for i,t,r,e,d,m in scenes],
 'required_types':['character','human','browser_proof','spreadsheet_proof','before_after','motion_graphics','cta'],
 'optional_patterns':['series_teaser only when the next part has a concrete payoff'],
 'hard_reject':['single-screen-dominant','slide-deck-feel','low-resolution-crop','static-scene-over-2.2s','missing-cinematic-assets','missing-operation-proof','generic-next-episode-preview']
}
Path('output').mkdir(exist_ok=True)
Path('output/v19_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
Path('output/v19_scene_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(plan,ensure_ascii=False))
