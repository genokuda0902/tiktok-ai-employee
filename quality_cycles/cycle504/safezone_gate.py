from dataclasses import dataclass
GENRES = tuple(range(10))
@dataclass(frozen=True)
class TextBox:
    left: int
    top: int
    right: int
    bottom: int
def text_fits_safe_zone(box, safe=(120,260,780,1250)):
    return safe[0]<=box.left<box.right<=safe[2] and safe[1]<=box.top<box.bottom<=safe[3]
def verify_text_boxes(boxes):
    boxes=list(boxes)
    if not boxes or not all(text_fits_safe_zone(x) for x in boxes):
        raise ValueError("Text outside safe area")
def publication_approved(qa):
    required={"full_decode":"PASS","native_japanese_voice":"HUMAN_VERIFIED","voice_caption_sync":"PASS","human_review":"APPROVED","publication":"MANUAL_POST_APPROVED"}
    return qa.get("resolution")==[1080,1920] and all(qa.get(k)==v for k,v in required.items())
