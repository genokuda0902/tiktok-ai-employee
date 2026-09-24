"""Zero-cost ChatGPT storyboard panel contract for TikTok image-first videos.

A generated 5x2 storyboard is treated only as an intermediate asset. Each cell is
cropped to 9:16 and rendered as an independent 1080x1920 scene. Publication
approval remains external and manual.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class PanelContract:
    rows: int = 2
    cols: int = 5
    width: int = 1080
    height: int = 1920
    scene_count: int = 10
    manual_post_only: bool = True
    requires_rights_approval: bool = True

    def validate(self) -> None:
        if self.rows * self.cols != self.scene_count:
            raise ValueError("panel grid must match scene_count")
        if (self.width, self.height) != (1080, 1920):
            raise ValueError("TikTok delivery must be 1080x1920")
        if not self.manual_post_only or not self.requires_rights_approval:
            raise ValueError("approval/manual-post gates must fail closed")


def crop_box(index: int, source_width: int, source_height: int,
             contract: PanelContract = PanelContract()):
    contract.validate()
    if not 0 <= index < contract.scene_count:
        raise IndexError(index)
    col, row = index % contract.cols, index // contract.cols
    x0 = round(col * source_width / contract.cols)
    x1 = round((col + 1) * source_width / contract.cols)
    y0 = round(row * source_height / contract.rows)
    y1 = round((row + 1) * source_height / contract.rows)
    return x0, y0, x1, y1
