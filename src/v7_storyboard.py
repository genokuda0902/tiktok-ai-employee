#!/usr/bin/env python3
"""AI時短ラボ v7: follower-first edit director.
Turns narration timing into a reusable multi-layer edit plan shared by all employee accounts.
"""
import json
from pathlib import Path
O=Path('output'); O.mkdir(exist_ok=True)
timing=json.loads((O/'narration_timing.json').read_text(encoding='utf-8'))
D=max(x['end'] for x in timing)
# visual grammar learned from supplied references: anchor -> proof -> UI -> reaction -> payoff -> CTA.
scenes=[
 {'role':'HOOK','start':0,'end':2.2,'layers':['robot_presenter','kinetic_headline','before_after'],'motion':'push_in','max_static':0.8},
 {'role':'PAIN','start':2.2,'end':6.0,'layers':['realistic_document','robot_reaction','highlight'],'motion':'pan_crop','max_static':1.5},
 {'role':'DEMO','start':6.0,'end':14.0,'layers':['browser_operation','cursor','typing','prompt_zoom'],'motion':'screen_punch','max_static':1.8},
 {'role':'PROOF','start':14.0,'end':21.0,'layers':['ai_result','table_reveal','copy_click'],'motion':'row_reveal','max_static':1.6},
 {'role':'PAYOFF','start':21.0,'end':min(27.0,D),'layers':['spreadsheet_operation','paste_proof','robot_celebrate'],'motion':'zoom_cut','max_static':1.5},
 {'role':'CTA','start':min(27.0,D-3),'end':D,'layers':['robot_presenter','save_reason','next_episode'],'motion':'push_in','max_static':1.4},
]
plan={'version':'v7','canvas':'1080x1920','fps':30,'brand':'AI時短ラボ','goal':'follower_growth',
      'rules':{'visual_change_sec_max':2.5,'hook_proof_sec_max':1.0,'real_operation_share_min':0.45,
               'character_share_range':[0.15,0.30],'one_primary_cta':True,'reference_copying':False},
      'scenes':scenes,'narration':timing}
(O/'v7_storyboard.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(plan,ensure_ascii=False))
