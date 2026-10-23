"""Shared 10-genre, 8-scene timing and guided-motion contract (cycle798).
No uploads, publishing, or paid API calls. Coordinates are local to art panel.
"""
WIDTH, HEIGHT, FPS = 1080, 1920, 30
SCENE_FRAMES = (57, 63, 58, 63, 40, 47, 48, 53)
ART_RECT = (35, 430, 1010, 1050)
SUBTITLE_SAFE_RECT = (30, 1530, 1020, 230)
GENRES = {
    'ai_work':'#9B90FF','beauty':'#E5ACD7','love_psychology':'#C0A2FF',
    'money_saving':'#6BE1B8','sales_business':'#58C5F6','career':'#83C5F9',
    'health_life':'#6EE7BE','science':'#39E7D3','travel_food':'#70D6EA',
    'product_life':'#C6A0F5',
}

def progress_at(local_frame, total_frames):
    if not 0 <= local_frame < total_frames:
        raise ValueError('frame outside scene')
    return (local_frame + 0.5) / total_frames

def attention_target(scene_index, progress):
    """Coordinates and radius of the currently highlighted instructional step."""
    if not 0 <= progress <= 1:
        raise ValueError('progress outside 0..1')
    step = min(2, int(progress * 3))
    if scene_index == 3:
        return 185, 192 + step * 196 + 83, 64
    if scene_index == 5:
        return 225 + step * 306, 453, 132
    return None

def validate_contract():
    x,y,w,h = ART_RECT
    sx,sy,sw,sh = SUBTITLE_SAFE_RECT
    return (len(GENRES)==10 and len(SCENE_FRAMES)==8 and sum(SCENE_FRAMES)==429
            and x>=0 and y>=0 and x+w<=WIDTH and y+h<=sy
            and sx>=0 and sy>=0 and sx+sw<=WIDTH and sy+sh<=HEIGHT)
