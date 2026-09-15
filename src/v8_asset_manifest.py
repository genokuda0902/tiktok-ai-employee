#!/usr/bin/env python3
"""v8 asset-first production contract.
Prevents the renderer from silently falling back to cheap slide-only output.
"""
import json
from pathlib import Path
O=Path('output'); O.mkdir(exist_ok=True)
manifest={
 'version':'v8','mode':'asset_first','brand':'AI時短ラボ',
 'reference_target':'presenter-led TikTok + real operation proof + fast visual variation',
 'required_capabilities':[
  'branded_robot_presenter_asset','operation_capture','kinetic_caption','before_after',
  'cursor_typing_click','punch_in_zoom','reaction_cut','sfx','next_episode_cta'],
 'scene_policy':{
  'hook':{'sec':[0,2],'primary':'robot_presenter','secondary':'instant_result'},
  'problem':{'sec':[2,5],'primary':'work_pain_visual'},
  'demo':{'sec':[5,18],'primary':'operation_capture','min_share':0.55},
  'proof':{'sec':[18,25],'primary':'before_after_result'},
  'cta':{'sec':[25,33],'primary':'robot_presenter'}},
 'quality_constraints':{
  'max_static_seconds':2.0,'max_caption_chars_per_phrase':20,
  'operation_share_min':0.50,'presenter_share_min':0.15,'presenter_share_max':0.30,
  'simple_shape_robot_forbidden':True,'slide_only_forbidden':True,
  'reference_identity_copy_forbidden':True}
}
(O/'v8_asset_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False))
