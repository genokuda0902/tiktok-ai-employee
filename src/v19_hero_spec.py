#!/usr/bin/env python3
import json
from pathlib import Path

heroes={
  '01_robot_hook':{'scenes':[1],'subject':'same young Japanese male protagonist plus AI時短ラボ glossy white rounded 3D robot, black glass face, cyan happy eyes and cyan accents','action':'man reaches toward camera while robot points at viewer','world':'premium cinematic Japanese office at night, cluttered paperwork, blue/cyan practical lights, shallow depth of field','camera':'vertical 9:16, close dynamic perspective, foreground hand, push-in safe composition'},
  '02_stressed_worker':{'scenes':[2],'subject':'same young Japanese male protagonist in dark modern business attire, photorealistic','action':'overwhelmed by repetitive paperwork and spreadsheet work, hands near temples','world':'same premium Japanese office desk, laptop and paperwork, practical warm/cool lighting','camera':'vertical 9:16, cinematic 50mm look, foreground papers, depth layers'},
  '03_robot_solution':{'scenes':[3],'subject':'same protagonist plus same glossy white/cyan robot','action':'robot confidently presents the solution while man turns attention to laptop','world':'same premium office with subtle blue technology lighting','camera':'vertical 9:16, dynamic three-quarter shot, gentle orbit-safe composition'},
  '09_before_after':{'scenes':[9],'subject':'same Japanese male protagonist, identical face/hair/wardrobe continuity','action':'before stressed at cluttered desk; after relaxed and smiling with completed work','world':'matched office environment, visual transformation from cluttered dark desk to clean bright workspace','camera':'vertical 9:16 transformation-safe framing'},
  '11_robot_cta':{'scenes':[11,13,15],'subject':'same protagonist plus same official glossy white/cyan robot','action':'friendly confident save gesture, thumbs-up/wave/open-arm variants','world':'cinematic cyan/blue brand environment with real depth and practical lighting','camera':'vertical 9:16, multiple crop-safe poses, strong silhouette'},
  '12_freedom':{'scenes':[12],'subject':'same Japanese male protagonist, consistent identity and wardrobe family','action':'calmly looks over the city after finishing work early, relaxed posture','world':'sunset-to-blue-hour generic Japanese city skyline, premium rooftop or window view','camera':'vertical 9:16 cinematic portrait with large clean subtitle-safe negative space'}
}
contract={'version':'v19','output':'independent high-resolution vertical hero assets','min_resolution':'1024x1792','preferred_resolution':'1080x1920 or higher','rules':['no storyboard collage','absolutely no embedded text or letters','no generated logos','consistent robot identity','consistent human identity','photorealistic human','premium 3D robot','depth and lighting required','motion-safe framing','one independent asset per hero key'],'heroes':heroes}
Path('output').mkdir(exist_ok=True)
Path('output/v19_hero_spec.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(contract,ensure_ascii=False,indent=2))
