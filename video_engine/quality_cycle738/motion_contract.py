"""Genre-agnostic smooth motion contract for a 220-frame workbook demonstration.

Synthetic-only visual geometry. No media, audio, user data or credentials.
This is a review-only component and is not the original v33 renderer.
"""
import bisect

PHASES = (28, 28, 28, 26, 28, 28, 28, 26)
START, END = 384, 604
CUMULATIVE = [0]
for n in PHASES:
    CUMULATIVE.append(CUMULATIVE[-1] + n)


def smoothstep(x):
    x = max(0.0, min(1.0, x))
    return x*x*(3.0-2.0*x)


def motion_spec(index):
    """Monotonic zoom/progress plus an eased pointer for each selected cell."""
    if not 0 <= index < END-START:
        raise ValueError('index outside scene')
    phase = min(bisect.bisect_right(CUMULATIVE,index)-1,len(PHASES)-1)
    local = (index-CUMULATIVE[phase])/max(1,PHASES[phase]-1)
    p = index/(END-START-1)
    zoom = 1.0 + 0.028*smoothstep(p)
    row = min(phase//2,3)
    prev_row = min(max(0,(phase-1)//2),3)
    target_y = 671+90*(row+1)+45
    prev_y = 671+90*(prev_row+1)+45
    blend = smoothstep(local/0.20) if phase in (2,4,6) else 1.0
    y = round(prev_y+(target_y-prev_y)*blend)
    x = round(905-45*smoothstep(local)) if phase%2==0 else round(860+45*smoothstep(local))
    return {'phase':phase,'row':row,'zoom':zoom,'cursor_x':x,'cursor_y':y,
            'progress':p,'bar_width':round(924*p)}
