from dataclasses import dataclass

@dataclass(frozen=True)
class StageLabelCleanup:
    x: int = 40
    y: int = 103
    width: int = 220
    height: int = 62

    def validate(self, frame_width: int, frame_height: int) -> None:
        if (frame_width, frame_height) != (1080, 1920):
            raise ValueError("requires 1080x1920")
        if self.width > 260 or self.height > 70:
            raise ValueError("mask exceeds safe region")

    def ffmpeg_filter(self) -> str:
        self.validate(1080, 1920)
        return f"drawbox=x={self.x}:y={self.y}:w={self.width}:h={self.height}:color=0xf3f7f6:t=fill"

def requires_human_approval() -> bool:
    return True

def automatic_posting_allowed() -> bool:
    return False
