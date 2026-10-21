"""Cycle746 reusable numeric/chart data contract. Review-only, ten genres.

Synthetic demonstration data. Never publish or auto-post. This module has
no dependency on previous MP4 or unapproved assets.
"""
from dataclasses import dataclass

GENRE_ACCENTS = {
    "ai_work": (75, 227, 218), "romance": (255, 148, 182),
    "beauty": (240, 182, 221), "money": (160, 220, 131),
    "trivia": (245, 197, 111), "gadgets": (116, 186, 253),
    "health": (116, 222, 175), "sales": (255, 167, 102),
    "travel": (117, 205, 241), "mystery": (183, 154, 255),
}

@dataclass(frozen=True)
class Month:
    label: str
    value: int

SAMPLE = (Month("1月", 12), Month("2月", 15),
          Month("3月", 20), Month("4月", 18))

def validate_data(data):
    if not data or len(data) > 12 or len({m.label for m in data}) != len(data):
        raise ValueError("month labels must be unique and nonempty; max 12")
    if any(not isinstance(m.label, str) or not m.label or
           type(m.value) is not int or m.value < 0 for m in data):
        raise ValueError("month data must have a label and nonnegative integer")
    if max(m.value for m in data) == 0:
        raise ValueError("chart cannot use an all-zero scale")
    return {"sum": sum(m.value for m in data),
            "max": max(m.value for m in data),
            "peak": max(data, key=lambda m: m.value).label}

def bar_geometry(data, baseline=1120, height=290):
    peak = validate_data(data)["max"]
    return tuple({"label": m.label, "value": m.value,
                  "top": baseline-round(height*m.value/peak),
                  "bottom": baseline} for m in data)

def publication_gate(meta):
    fields = ("source_approved", "privacy_checked", "employee_approved",
              "audio_rights_checked", "caption_sync_checked", "phone_checked")
    return all(meta.get(k) is True for k in fields) and meta.get("manual_post_only") is True
