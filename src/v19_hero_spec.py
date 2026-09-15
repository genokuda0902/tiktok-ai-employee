#!/usr/bin/env python3
import json
from pathlib import Path

# These prompts are production contracts for an image/video generation layer.
# No embedded Japanese text: typography is added later for reliability.
heroes={
  '01_robot_hook':{'scenes':[1],'subject':'AI時短ラボ official glossy white rounded 3D robot, black glass face, cyan happy eyes, cyan accents','action':'leans toward camera and points at viewer','world':'premium cinematic Japanese office at night, blue/cyan practical lights, shallow depth of field','camera':'vertical 9:16, medium close-up, low-angle push-in safe composition'},
  '02_stressed_worker':{'scenes':[2],'subject':'young Japanese male office worker in modern business attire, realistic photography','action':'overwhelmed by repetitive paperwork and spreadsheet work, hands near temples','world':'real Japanese office desk, laptop, paperwork, natural practical lighting','camera':'vertical 9:16, cinematic 50mm look, foreground papers, depth layers'},
  '03_robot_solution':{'scenes':[3],'subject':'same AI時短ラボ glossy white/cyan 3D robot','action':'confident wink and presents laptop/workflow with one hand','world':'premium blue technology office, volumetric rim light, subtle particles','camera':'vertical 9:16, dynamic three-quarter shot, gentle orbit safe composition'},
  '09_before_after':{'scenes':[9],'subject':'same Japanese office worker, consistent identity and wardrobe','action':'before stressed at cluttered desk; after relaxed and smiling at clean desk with completed work','world':'matched office environment, visual transformation from gray clutter to bright clean blue daylight','camera':'vertical 9:16 split/transformation-safe framing'},
  '11_robot_cta':{'scenes':[11,13,16],'subject':'same AI時短ラボ official 3D robot','action':'friendly thumbs-up, wave, welcoming open-arm poses','world':'cinematic cyan/blue brand space with depth, light streaks and soft particles','camera':'vertical 9:16, multiple crop-safe poses, strong center silhouette'},
  '12_device_next':{'scenes':[12],'subject':'premium laptop on modern desk with AI時短ラボ robot beside it','action':'robot gestures toward presentation slides on laptop','world':'warm premium office with blue accent lights','camera':'vertical 9:16 commercial product shot, shallow depth of field'},
  '14_city_message':{'scenes':[14],'subject':'Japanese professional looking over modern city skyline from office window','action':'calm confident posture suggesting more freedom from repetitive work','world':'sunset-to-blue-hour Osaka/Tokyo-like generic Japanese city, no identifiable landmark required','camera':'vertical 9:16 cinematic silhouette and reflection layers'}
}
contract={'version':'v19','output':'independent high-resolution vertical hero assets','min_resolution':'1024x1792','preferred_resolution':'1080x1920 or higher','rules':['no storyboard collage','no embedded Japanese text','no logos unless supplied as licensed brand asset','consistent robot identity','consistent human identity for before/after','photorealistic humans','premium 3D robot','depth and lighting required','motion-safe framing'],'heroes':heroes}
Path('output').mkdir(exist_ok=True)
Path('output/v19_hero_spec.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2))
print(json.dumps(contract,ensure_ascii=False,indent=2))
