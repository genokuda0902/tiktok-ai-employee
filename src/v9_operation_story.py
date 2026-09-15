#!/usr/bin/env python3
import json
from pathlib import Path
story={"version":"v9","operation":{"start":5.5,"end":21.5,"screen_share":1.0,"beats":[
{"t":[5.5,7.4],"action":"type_prompt","focus":"prompt_box","zoom":1.00,"cursor":True,"caption":"この文章を表に"},
{"t":[7.4,9.2],"action":"highlight_fields","focus":"氏名・電話・メール・希望日時","zoom":1.12,"cursor":True,"caption":"欲しい項目を指定"},
{"t":[9.2,10.3],"action":"click_send","focus":"send_button","zoom":1.25,"cursor":True,"sfx":"click"},
{"t":[10.3,12.2],"action":"generation","focus":"response","zoom":1.05,"cursor":False,"caption":"すると…"},
{"t":[12.2,14.4],"action":"table_reveal","focus":"first_rows","zoom":1.10,"cursor":False,"caption":"一瞬で表に"},
{"t":[14.4,16.1],"action":"table_complete","focus":"all_rows","zoom":1.00,"cursor":False,"caption":"整形まで完了"},
{"t":[16.1,17.5],"action":"click_copy","focus":"copy_button","zoom":1.28,"cursor":True,"sfx":"click"},
{"t":[17.5,18.8],"action":"switch_excel","focus":"sheet","zoom":1.00,"transition":"whip"},
{"t":[18.8,20.0],"action":"paste","focus":"A1:D4","zoom":1.18,"cursor":True,"sfx":"paste_hit"},
{"t":[20.0,21.5],"action":"proof_hold","focus":"finished_table","zoom":1.08,"caption":"手入力ほぼ不要"}
]},"rules":{"fake_brand_chrome":False,"show_realistic_workflow":True,"no_tiny_window":True,"visual_change_max":1.9,"cursor_motion":True,"typing_animation":True,"click_feedback":True,"result_reveal":True}}
out=Path('output');out.mkdir(exist_ok=True)
(out/'v9_operation_story.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf-8')
print('v9 operation story ready: 10 proof beats')
