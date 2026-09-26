"""Deterministic spreadsheet UI layer for image-first TikTok slides.

Replaces AI-generated UI text regions with verified Japanese text rendered by the
video pipeline. This is a reimplementation helper: no external upload, paid API,
or automatic posting.
"""
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class SpreadsheetRow:
    date: str
    product: str
    sales: int
    count: int

def validate_rows(rows: Sequence[SpreadsheetRow]) -> None:
    if not 3 <= len(rows) <= 12:
        raise ValueError("spreadsheet demo requires 3-12 rows")
    for row in rows:
        if not row.date.strip() or not row.product.strip():
            raise ValueError("blank deterministic UI text")
        if row.sales < 0 or row.count < 0:
            raise ValueError("negative demo values are not allowed")

def release_contract() -> dict:
    return {
        "zero_cost": True,
        "deterministic_text_layer": True,
        "ai_generated_ui_text_allowed": False,
        "portrait_delivery": (1080, 1920),
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
