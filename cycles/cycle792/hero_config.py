"""cycle792: reusable 10-genre 9:16 hero and safe-area configuration.

Full PIL/ffmpeg render implementation and source audio are distributed in the
local review ZIP. The GitHub CI smoke video is synthetic and not the final
Japanese-narrated human-review MP4.
"""
WIDTH=1080
HEIGHT=1920
FPS=30
HOOK_FRAMES=60
TOTAL_FRAMES=429
ARTWORK_BOX=(64,456,1016,1360)
CAPTION_SAFE_BOX=(75,1400,1005,1540)
PALETTES={
 'ai_work':'#35e8d2',
 'beauty':'#f0a5d8',
 'relationships':'#ff98b9',
 'saving':'#79d7ff',
 'sales_business':'#ffd176',
 'career':'#77e2c4',
 'health':'#77dbbd',
 'science':'#35e8d2',
 'travel_food':'#ffa877',
 'product_lifestyle':'#a8cfff',
}
def safe_boxes_do_not_overlap():
 x1,y1,x2,y2=ARTWORK_BOX
 a1,b1,a2,b2=CAPTION_SAFE_BOX
 return x2<=a1 or a2<=x1 or y2<=b1 or b2<=y1

def validate():
 assert (WIDTH,HEIGHT,FPS)==(1080,1920,30)
 assert TOTAL_FRAMES==429 and HOOK_FRAMES==60
 assert len(PALETTES)==10
 assert all(v.startswith('#') and len(v)==7 for v in PALETTES.values())
 assert safe_boxes_do_not_overlap()
 return True
