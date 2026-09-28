from dataclasses import dataclass


@dataclass(frozen=True)
class JapaneseHookFontGuard:
    font_path: str = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    start: float = 0.0
    end: float = 1.8
    width: int = 1080
    height: int = 1920

    def validate(self) -> None:
        if (self.width, self.height) != (1080, 1920):
            raise ValueError("delivery geometry must be 1080x1920")
        if not (0 <= self.start < self.end <= 3.0):
            raise ValueError("hook repair must stay inside first three seconds")
        if "NotoSansCJK" not in self.font_path:
            raise ValueError("Japanese-capable Noto CJK font is required")

    def filters(self, title: str, hook: str) -> str:
        self.validate()
        if not title.strip() or not hook.strip():
            raise ValueError("title and hook are required")
        if len(title) > 24 or len(hook) > 16:
            raise ValueError("hook copy too long for safe layout")
        enable = f"lt(t,{self.end})"
        return (
            "drawbox=x=0:y=120:w=1080:h=310:color=0xF7FBFC:t=fill:"
            f"enable='{enable}',"
            f"drawtext=fontfile={self.font_path}:text='{title}':fontcolor=0x08111D:"
            f"fontsize=62:x=(w-text_w)/2:y=155:enable='{enable}',"
            f"drawtext=fontfile={self.font_path}:text='{hook}':fontcolor=0x08111D:"
            f"fontsize=50:x=(w-text_w)/2:y=260:enable='{enable}'"
        )


def release_contract() -> dict:
    return {
        "zero_cost": True,
        "japanese_font_required": True,
        "preserve_audio": True,
        "human_approval_required": True,
        "auto_post": False,
    }
