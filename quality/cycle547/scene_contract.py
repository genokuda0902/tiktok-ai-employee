"""Cycle547 synthetic-data visual QA contract. Review only."""
GENRES = ("ai_work","beauty","relationships","finance","sales_business","career","health_lifestyle","science_trivia","travel_food","shopping_lifestyle")
def check_scene(c):
    if c.get("genre") not in GENRES:
        raise ValueError("unsupported genre")
    if c.get("asset_status") != "synthetic_review_only":
        raise ValueError("unapproved source")
    if c.get("publication_status") != "NOT_APPROVED":
        raise ValueError("publication is prohibited")
    if c.get("data_is_real") is not False:
        raise ValueError("real data not permitted")
    values = c.get("values")
    if not isinstance(values,list) or len(values) != 4 or any(type(v) is not int or v<1 or v>9999 for v in values):
        raise ValueError("invalid data")
    if c.get("total") != sum(values):
        raise ValueError("data/total mismatch")
    return True
