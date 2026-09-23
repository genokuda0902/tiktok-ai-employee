"""Zero-cost pacing helper for baked 1080x1920 TikTok image cards.

Text, BEFORE/AFTER and CTA remain baked into source images. This module only
assigns deterministic durations, subtle motion and optional micro-fades so the
same route can be reused across ten genres. Human quality/rights approval
remains mandatory.
"""


def paced_cards(cards, width: int = 1080, height: int = 1920, default_duration: float = 2.0):
    if (width, height) != (1080, 1920):
        raise ValueError("paced image slides require 1080x1920")
    if not cards or default_duration <= 0:
        raise ValueError("cards and a positive duration are required")
    out = []
    for index, card in enumerate(cards):
        image = str(card.get("image", "")).strip()
        caption = str(card.get("caption", "")).strip()
        if not image or not caption:
            raise ValueError(f"card {index} requires image and baked caption")
        duration = float(card.get("duration", default_duration))
        if duration < 1.2 or duration > 4.0:
            raise ValueError("card duration must stay between 1.2 and 4.0 seconds")
        motion = "zoom_in" if index % 2 == 0 else "zoom_out"
        out.append({"image": image, "caption": caption, "duration": duration,
                    "motion": motion, "text_baked": True})
    return tuple(out)


def zoompan_filter(motion: str, fps: int = 30) -> str:
    if motion not in {"zoom_in", "zoom_out"} or fps <= 0:
        raise ValueError("invalid motion/fps")
    if motion == "zoom_in":
        z = "min(zoom+0.00035,1.018)"
    else:
        z = "if(eq(on,1),1.018,max(zoom-0.00035,1.0))"
    return f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps}"


def micro_fade_filter(duration: float, fade: float = 0.06) -> str:
    """Return a short fade-in/out filter for a baked card.

    The fade is intentionally tiny: it softens hard slide cuts without making
    captions, comparison numbers or CTA text unreadable. It is genre-agnostic.
    """
    duration = float(duration)
    fade = float(fade)
    if duration < 1.2 or duration > 4.0:
        raise ValueError("card duration must stay between 1.2 and 4.0 seconds")
    if fade <= 0 or fade > 0.12 or fade * 2 >= duration:
        raise ValueError("micro fade must be >0, <=0.12s and shorter than the card")
    out_start = duration - fade
    return f"fade=t=in:st=0:d={fade:.2f},fade=t=out:st={out_start:.2f}:d={fade:.2f}"
