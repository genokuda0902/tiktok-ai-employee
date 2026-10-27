"""Cycle883 local-only proof zoom and ten-genre timeline core."""
from dataclasses import dataclass
W,H,FPS,FRAMES=1080,1920,30,691
CAPTION_BAND=(1435,1715)
GENRES=(
 'ai_productivity','beauty','romance_psychology','money_saving',
 'sales_business','career','health_lifestyle','trivia_science',
 'travel_food','product_lifestyle',
)
SCENE_BOUNDS=(0,93,176,254,341,426,518,596,691)
SCENE_STATES={
 1:(0,24,56,93),2:(93,118,145,176),3:(176,254),
 4:(254,270,287,304,321,341),5:(341,358,375,392,409,426),
 6:(426,518),7:(518,544,570,596),8:(596,691),
}
SCREENSHOTS={
 4:('chromium_prompt_initial','chromium_prompt_goal','chromium_prompt_rule','chromium_prompt_style','chromium_prompt_confirmed'),
 5:('chromium_review_initial','chromium_review_number','chromium_review_content','chromium_review_expression','chromium_review_approved'),
 7:('chromium_save_initial','chromium_save_focused','chromium_save_saved'),
}
CROP_BOX={4:(45,115,620,575),5:(45,115,620,575),7:(45,115,620,575)}
FOCUS_WIDTH=920

@dataclass(frozen=True)
class Clip:
 scene:int
 stage:int
 start:int
 end:int
 source:str

def timeline():
 out=[]
 for scene,bounds in SCENE_STATES.items():
  for stage,(start,end) in enumerate(zip(bounds,bounds[1:])):
   src=SCREENSHOTS[scene][stage] if scene in SCREENSHOTS else f'slide_{scene:02d}'
   out.append(Clip(scene,stage,start,end,src))
 return tuple(out)

def zoom_factor(scene):
 x0,_,x1,_=CROP_BOX[scene]
 return FOCUS_WIDTH/(x1-x0)

def validate(genre='ai_productivity',clips=None):
 if genre not in GENRES:raise ValueError('unknown genre')
 clips=timeline() if clips is None else tuple(clips)
 if len(clips)!=22 or clips[0].start!=0 or clips[-1].end!=FRAMES:raise ValueError('bad duration/state count')
 for i,c in enumerate(clips):
  if c.start>=c.end or c.scene<1 or c.scene>8:raise ValueError('invalid clip')
  if i and clips[i-1].end!=c.start:raise ValueError('gap/overlap')
  if i and clips[i-1].scene>c.scene:raise ValueError('scene out of order')
 for scene in SCREENSHOTS:
  if zoom_factor(scene)<1.5:raise ValueError('zoom too small')
  x0,y0,x1,y1=CROP_BOX[scene]
  if not(0<=x0<x1<=860 and 0<=y0<y1<=690):raise ValueError('crop outside source')
 if CAPTION_BAND[0]<1400 or CAPTION_BAND[1]>1750:raise ValueError('unsafe captions')
 return True

def safe_source(provenance,external_network=False,personal_data=False):
 if provenance!='locally authored HTML / offline Chromium screenshots' or external_network or personal_data:
  raise ValueError('source requires rights/privacy review')
 return True
