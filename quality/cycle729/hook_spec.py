"""Ten-genre quality contract for cycle729 opening hook."""
WIDTH=1080
HEIGHT=1920
FPS=30
HOOK_FRAMES=78
SAFE_RIGHT=900
SAFE_BOTTOM=1605
CAPTION_RIGHT=876
CAPTION_BOTTOM=1525
CUES=((0.1667,1.0,'この基板、'),(1.0,1.8667,'実はパソコン。'))
def caption_at(t):
    return next((v for a,b,v in CUES if a<=t<b),'')

def validate():
    return (WIDTH,HEIGHT,FPS)==(1080,1920,30) and HOOK_FRAMES==78 and CAPTION_RIGHT<=SAFE_RIGHT and CAPTION_BOTTOM<=SAFE_BOTTOM
