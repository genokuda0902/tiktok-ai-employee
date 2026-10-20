"""Cycle705 fictional sales proof and reusable 10-genre publication gates."""
MONTHS = ("1月", "2月", "3月", "4月")
SALES = (120000, 150000, 200000, 180000)
YOY = (110, 115, 120, 118)
GENRE_SLOTS = tuple(f"genre_{i:02d}" for i in range(1, 11))
SCENES = (
    (0, 2.5, "売上グラフ、まだ手作業？"),
    (2.5, 5, "まず4か月のデータを用意"),
    (5, 7.5, "AIに分析を依頼"),
    (7.5, 10, "グラフと要点を整理"),
    (10, 12.5, "3月が最高：20万円"),
    (12.5, 15, "Excelで使える形に"),
    (15, 17.5, "4か月の売上推移が完成"),
    (17.5, 20, "保存してあとで試そう"),
)
PROMPT = "この売上データを分析して\nグラフと要点をまとめて\nExcelで使える形式で出力して"

def evidence():
    peak = max(SALES)
    idx = SALES.index(peak)
    return {"peak_month": MONTHS[idx], "peak_yen": peak,
            "total_yen": sum(SALES),
            "feb_to_mar_growth_pct": round((SALES[2]/SALES[1]-1)*100, 1)}

def validate_story():
    assert len(MONTHS) == len(SALES) == len(YOY) == 4
    assert len(GENRE_SLOTS) == 10
    assert len(SCENES) == 8
    assert SCENES[0][0] == 0 and SCENES[-1][1] == 20
    assert all(a < b and (i == 0 or a == SCENES[i-1][1]) for i, (a,b,_) in enumerate(SCENES))
    assert evidence() == {"peak_month":"3月", "peak_yen":200000,"total_yen":650000,"feb_to_mar_growth_pct":33.3}
    return True

def can_publish(*, source_approved, privacy_checked, employee_approved,
                narration_verified, captions_synced, phone_checked):
    return all((source_approved, privacy_checked, employee_approved,
                narration_verified, captions_synced, phone_checked))

def asset_gate(assets):
    allowed = {"self_generated", "licensed", "public_domain"}
    return bool(assets) and all(a.get("origin") in allowed and a.get("approved") is True for a in assets)
