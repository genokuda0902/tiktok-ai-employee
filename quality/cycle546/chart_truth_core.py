"""Cycle546 reusable data-to-chart correctness gate; review-only."""
GENRES=("ai_work","beauty","relationships","finance","sales_business","career","health_lifestyle","science_trivia","travel_food","shopping_lifestyle")
def validate(config):
    if config.get("genre") not in GENRES:
        raise ValueError("Unknown genre")
    if config.get("asset_status") != "synthetic_review_only":
        raise ValueError("Rights status not approved for review")
    if config.get("publication_status") != "NOT_APPROVED":
        raise ValueError("Publication status must remain unapproved")
    labels, values = config.get("labels"), config.get("values")
    if not isinstance(labels,list) or len(labels)!=4 or any(not isinstance(s,str) or not 1<=len(s)<=6 for s in labels):
        raise ValueError("Four short labels required")
    if not isinstance(values,list) or len(values)!=4 or any(type(v) is not int or not 1<=v<=9999 for v in values):
        raise ValueError("Four positive integer values required")
    if sum(values)!=config.get("total"):
        raise ValueError("Arithmetic mismatch")
    return True

def bar_heights(values, maximum=180):
    if len(values)!=4 or any(type(v) is not int or v<=0 for v in values):
        raise ValueError("Invalid values")
    return [round(v/max(values)*maximum) for v in values]
