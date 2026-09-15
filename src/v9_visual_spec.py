#!/usr/bin/env python3
import json
from pathlib import Path
spec={
 "version":"v9",
 "goal":"reference-level presenter-led TikTok, not slide-deck motion graphics",
 "render":{"size":[1080,1920],"fps":30,"max_unchanged_seconds":1.6},
 "visual_mix":{"operation_proof_min":0.45,"presenter":0.20,"before_after":0.10,"supporting_visuals":0.25},
 "required_shots":[
  {"id":"hook","seconds":[0,2.2],"visual":"dramatic robot close-up + finished Excel result immediately","camera":"fast push-in"},
  {"id":"pain","seconds":[2.2,5.5],"visual":"messy customer text / manual copy","camera":"handheld-like crop changes"},
  {"id":"operation","seconds":[5.5,17.5],"visual":"full-screen AI operation with typing, click, response","camera":"screen punch-ins at proof moments"},
  {"id":"proof","seconds":[17.5,23.5],"visual":"AI table -> Excel paste transformation","camera":"match cut + zoom"},
  {"id":"reaction","seconds":[23.5,27.0],"visual":"robot reaction + large benefit text","camera":"medium to close"},
  {"id":"cta","seconds":[27.0,33.0],"visual":"robot + save CTA + next episode preview","camera":"slow push-in"}
 ],
 "presenter":{"identity":"AI時短ラボ official white 3D robot, black face panel, cyan glow, laptop AI","poses":["hook_point","explain","surprised","celebrate","cta_save"],"forbid":["flat rectangle robot","single static pose","generic human presenter"]},
 "editing":{"caption_chars_max":18,"caption_lines_max":2,"camera_change_seconds_max":2.0,"proof_before_second":2.2,"operation_fullscreen":True,"use_depth":True,"use_sfx":True,"use_transition_hits":True},
 "hard_fail":["slide_only","operation_window_too_small","flat_shape_presenter","no_visual_change_over_2s","proof_after_3s","reference_identity_copy"]
}
out=Path('output'); out.mkdir(exist_ok=True)
(out/'v9_visual_spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
print('v9 visual contract ready')
