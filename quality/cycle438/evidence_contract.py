"""Deterministic, genre-neutral proof validator for numeric video claims.
Does not imply human quality approval. All example data must be fictional.
"""
from decimal import Decimal, InvalidOperation


def calculate_claims(rows):
    amounts = [(str(r["key"]), Decimal(str(r["amount"]))) for r in rows]
    unique = dict(amounts)
    raw = sum((a for _, a in amounts), Decimal(0))
    dedup = sum(unique.values(), Decimal(0))
    return {"raw_total": int(raw), "unique_total": int(dedup),
            "difference": int(raw - dedup), "input_count": len(rows),
            "unique_count": len(unique), "duplicate_count": len(rows)-len(unique)}


def validate_proof(proof):
    rows = proof.get("rows")
    if not isinstance(rows, list) or not rows:
        return ["ROWS_MISSING"]
    if len(rows) > 5000:
        return ["ROWS_TOO_LARGE"]
    errors, values, seen, duplicates = [], [], set(), []
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or not {"key", "amount"} <= row.keys():
            errors.append(f"ROW_SCHEMA_{i}")
            continue
        key = str(row["key"]).strip()
        try:
            amount = Decimal(str(row["amount"]))
            if not amount.is_finite() or amount < 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError, TypeError):
            errors.append(f"ROW_AMOUNT_{i}")
            continue
        if not key:
            errors.append(f"ROW_KEY_{i}")
            continue
        values.append((key, amount))
        if key in seen:
            duplicates.append(key)
        seen.add(key)
    if errors:
        return errors
    grouped = {}
    for key, amount in values:
        if key in grouped and grouped[key] != amount:
            errors.append("KEY_AMOUNT_CONFLICT")
        grouped.setdefault(key, amount)
    if errors:
        return errors
    raw = sum((a for _, a in values), Decimal(0))
    dedup = sum(grouped.values(), Decimal(0))
    expected = {"raw_total": raw, "unique_total": dedup,
                "difference": raw-dedup, "input_count": len(values),
                "unique_count": len(grouped), "duplicate_count": len(duplicates)}
    claims = proof.get("claims", {})
    for name, actual in expected.items():
        try:
            claim = Decimal(str(claims[name]))
        except (KeyError, InvalidOperation, TypeError, ValueError):
            errors.append(f"CLAIM_MISSING_{name}")
            continue
        if claim != actual:
            errors.append(f"CLAIM_MISMATCH_{name}")
    if proof.get("data_class") != "FICTIONAL":
        errors.append("DATA_CLASS_NOT_APPROVED")
    if proof.get("assets") != "ORIGINAL_ONLY":
        errors.append("ASSET_RIGHTS_NOT_APPROVED")
    if proof.get("publication") != "NOT_APPROVED" or proof.get("auto_post") is not False:
        errors.append("UNSAFE_PUBLICATION")
    return errors
