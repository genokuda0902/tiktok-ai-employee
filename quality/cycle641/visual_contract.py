"""Review-only ten-genre video contract, cycle641. No publishing."""
from dataclasses import dataclass
GENRES=("AI仕事効率化","雑学","科学","心理","ビジネス","お金","歴史","ライフハック","テクノロジー","ミニチュア")
FPS=30
WIDTH=1080
HEIGHT=1920
FRAME_COUNT=600
SCENES=8

@dataclass(frozen=True)
class ReviewContract:
    asset_sha256: str
    usage: str="LOCAL_USER_REVIEW_ONLY"
    rights: str="UNVERIFIED"
    quality: str="HUMAN_REVIEW"
    publication: str="NOT_APPROVED"
    auto_post: bool=False
    narration: str="ABSENT"

def validate(c):
    if len(c.asset_sha256)!=64 or any(v not in "0123456789abcdef" for v in c.asset_sha256):
        raise ValueError("invalid asset digest")
    if (c.usage,c.rights,c.quality,c.publication,c.auto_post,c.narration)!=(
        "LOCAL_USER_REVIEW_ONLY","UNVERIFIED","HUMAN_REVIEW","NOT_APPROVED",False,"ABSENT"):
        raise ValueError("approval gate not satisfied")
    return len(GENRES)==10 and FRAME_COUNT==FPS*20

def scene_for_frame(frame):
    if type(frame)!=int or not 0<=frame<FRAME_COUNT:
        raise ValueError("frame out of bounds")
    return frame//75

def numeric_proof():
    return sum((120,150,200,180))==650
