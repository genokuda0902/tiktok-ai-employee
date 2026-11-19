"""Reusable, synthetic-only Excel tutorial scene state. No publication approval."""
VALUES = (1000, 2000, 3000, 4000)
STEPS = ("合計セルを選択", "関数を入力", "範囲を確認", "結果を表示")

def scene_state(seconds: float):
    """Deterministic four-stage timeline for any renderer."""
    if not 0 <= seconds < 12:
        raise ValueError("seconds must be in [0, 12)")
    index = int(seconds // 3)
    return {
        "index": index,
        "heading": STEPS[index],
        "highlight": "source_range" if index == 2 else "destination_cell",
        "formula": "=SUM(B2:B5)" if index >= 1 else "",
        "result": sum(VALUES) if index == 3 else None,
        "narration_verified": False,
        "publication_approved": False,
    }
