"""Reusable 10-genre, rights-gated, caption-safe scene transitions.

No network, external UI, auto-posting, or paid services.
"""
from dataclasses import dataclass

FPS = 30
FRAME_COUNT = 691
DISSOLVE_FRAMES = 6
SCENE_BOUNDS = (0, 93, 176, 254, 341, 426, 518, 596, 691)
SCENE_STATES = {
    1: (0, 24, 56, 93), 2: (93, 118, 145, 176), 3: (176, 254),
    4: (254, 270, 287, 304, 321, 341),
    5: (341, 358, 375, 392, 409, 426),
    6: (426, 518), 7: (518, 544, 570, 596), 8: (596, 691),
}
GENRES = (
    'ai_productivity', 'beauty', 'romance_psychology', 'money_saving',
    'sales_business', 'career', 'health_lifestyle', 'trivia_science',
    'travel_food', 'product_lifestyle',
)

@dataclass(frozen=True)
class Segment:
    kind: str
    scene: int
    stage: int
    frames: int
    step: int = 0


def smoothstep(t):
    """C1-continuous dissolve envelope (0 <= t <= 1)."""
    if not 0 <= t <= 1:
        raise ValueError('transition weight outside [0,1]')
    return t * t * (3 - 2 * t)


def transition_alpha(step, n=DISSOLVE_FRAMES):
    if not 1 <= step <= n or n < 2:
        raise ValueError('invalid dissolve step')
    return smoothstep(step / (n + 1))


def plan(genre='ai_productivity', dissolve=DISSOLVE_FRAMES):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    if not 2 <= dissolve <= 8:
        raise ValueError('dissolve length unsafe')
    result = []
    for scene, bounds in SCENE_STATES.items():
        for stage, (start, end) in enumerate(zip(bounds, bounds[1:])):
            last = end == SCENE_BOUNDS[scene]
            count = end - start - (dissolve if last and scene < 8 else 0)
            if count < 1:
                raise ValueError('not enough frames for dissolve')
            result.append(Segment('still', scene, stage, count))
            if last and scene < 8:
                for step in range(1, dissolve + 1):
                    result.append(Segment('dissolve', scene, stage, 1, step))
    if sum(x.frames for x in result) != FRAME_COUNT:
        raise ValueError('frame count changed')
    if sum(x.kind == 'dissolve' for x in result) != 7 * dissolve:
        raise ValueError('scene transition count changed')
    return tuple(result)


def source_gate(*, provenance, personal_data=False, external_network=False,
                rights_confirmed=False, publication_approved=False):
    """Rendering allowed for internal review; publishing is ALWAYS a separate manual gate."""
    if provenance != 'prior-cycle locally authored slides and mock Chromium UI':
        raise ValueError('unapproved asset provenance')
    if personal_data or external_network:
        raise ValueError('private or external source not allowed')
    if publication_approved and not rights_confirmed:
        raise ValueError('cannot approve publication without source rights')
    return {'render_internal_review': True, 'publication_approved': bool(publication_approved and rights_confirmed)}


def validate_caption_layout(x, y, width, height):
    if not (0 <= x and x + width <= 1080 and 1425 <= y and y + height <= 1720):
        raise ValueError('caption outside reserved safe band')
    return True
