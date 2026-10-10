from dataclasses import dataclass
from math import sin

@dataclass(frozen=True)
class Pose:
    center_x: int
    center_y: int
    size: int

POSES = {
    'hook': Pose(515, 625, 290),
    'result': Pose(558, 910, 132),
    'cta': Pose(545, 810, 185),
}

def mascot_pose(scene: str, t: float) -> Pose | None:
    if scene not in POSES:
        return None
    p = POSES[scene]
    return Pose(p.center_x, p.center_y + round(7 * sin(t * 2.7)), p.size)

def safe_for_caption(pose: Pose, caption_top: int = 1010) -> bool:
    return pose.center_y + pose.size // 2 < caption_top
