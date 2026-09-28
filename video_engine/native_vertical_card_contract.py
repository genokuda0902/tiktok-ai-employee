"""Zero-cost contract for native 1080x1920 image-first TikTok cards."""

from dataclasses import dataclass


@dataclass(frozen=True)
class NativeVerticalCard:
    width: int = 1080
    height: int = 1920
    max_title_chars: int = 24
    max_body_chars: int = 48
    safe_left: int = 70
    safe_right: int = 70
    safe_top: int = 110
    safe_bottom: int = 120

    def validate(self) -> None:
        if (self.width, self.height) != (1080, 1920):
            raise ValueError("native vertical cards must be 1080x1920")
        if min(self.safe_left, self.safe_right, self.safe_top, self.safe_bottom) < 60:
            raise ValueError("unsafe edge margin")
        if self.max_title_chars > 28 or self.max_body_chars > 60:
            raise ValueError("copy density too high for mobile reading")


def release_policy() -> dict:
    return {
        "zero_cost": True,
        "image_first": True,
        "native_1080x1920": True,
        "human_rights_approval_required": True,
        "human_quality_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
