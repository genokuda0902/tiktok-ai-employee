"""Regression tests for cycle438 numeric claims; no user data or publication."""
from copy import deepcopy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evidence_contract import calculate_claims, validate_proof

ROWS = [
    {"key":"A-101","amount":120000},
    {"key":"B-102","amount":150000},
    {"key":"C-103","amount":90000},
    {"key":"B-102","amount":150000},
    {"key":"D-104","amount":180000},
]

def valid():
    return {"rows":deepcopy(ROWS), "claims":calculate_claims(ROWS),
            "data_class":"FICTIONAL","assets":"ORIGINAL_ONLY",
            "publication":"NOT_APPROVED","auto_post":False}

def test_arithmetic():
    assert calculate_claims(ROWS)=={"raw_total":690000,"unique_total":540000,
        "difference":150000,"input_count":5,"unique_count":4,"duplicate_count":1}

def test_valid():
    assert validate_proof(valid())==[]

def test_bad_difference():
    p=valid();p["claims"]["difference"]=140000
    assert "CLAIM_MISMATCH_difference" in validate_proof(p)

def test_bad_count():
    p=valid();p["claims"]["duplicate_count"]=2
    assert "CLAIM_MISMATCH_duplicate_count" in validate_proof(p)

def test_conflicting_same_key():
    p=valid();p["rows"]=[{"key":"A","amount":1},{"key":"A","amount":2}]
    assert "KEY_AMOUNT_CONFLICT" in validate_proof(p)

def test_real_data_rejected():
    p=valid();p["data_class"]="REAL_CUSTOMERS"
    assert "DATA_CLASS_NOT_APPROVED" in validate_proof(p)

def test_unknown_rights_rejected():
    p=valid();p["assets"]="UNKNOWN"
    assert "ASSET_RIGHTS_NOT_APPROVED" in validate_proof(p)

def test_auto_post_rejected():
    p=valid();p["auto_post"]=True
    assert "UNSAFE_PUBLICATION" in validate_proof(p)

def test_premature_approval_rejected():
    p=valid();p["publication"]="APPROVED"
    assert "UNSAFE_PUBLICATION" in validate_proof(p)

def test_nan_rejected():
    p=valid();p["rows"][0]["amount"]="NaN"
    assert "ROW_AMOUNT_0" in validate_proof(p)

def test_negative_rejected():
    p=valid();p["rows"][0]["amount"]=-1
    assert "ROW_AMOUNT_0" in validate_proof(p)

def test_missing_rows_rejected():
    p=valid();p["rows"]=[]
    assert validate_proof(p)==["ROWS_MISSING"]
