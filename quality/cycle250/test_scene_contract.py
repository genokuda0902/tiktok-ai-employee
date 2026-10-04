from quality.cycle250.scene_contract import validate_scene_plan

def good_plan():
    return {
        "target_seconds": 15,
        "publication_gate": "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED",
        "scenes": [
            {"role":"HOOK","seconds":1.5,"purpose":"result first","visual_change":"result card","asset_approved":True},
            {"role":"PAIN","seconds":2.5,"purpose":"problem","visual_change":"before","asset_approved":True},
            {"role":"SOLUTION","seconds":3,"purpose":"action","visual_change":"operation","asset_approved":True},
            {"role":"PROOF","seconds":4,"purpose":"evidence","visual_change":"before-after","asset_approved":True},
            {"role":"VALUE","seconds":2,"purpose":"meaning","visual_change":"summary","asset_approved":True},
            {"role":"CTA","seconds":2,"purpose":"next action","visual_change":"cta","asset_approved":True},
        ],
    }

def test_valid_plan_passes():
    assert validate_scene_plan(good_plan()) == []

def test_missing_proof_fails_closed():
    p=good_plan()
    p["scenes"][3]["role"]="VALUE"
    assert "PROOF scene required" in validate_scene_plan(p)

def test_unapproved_asset_fails_closed():
    p=good_plan()
    p["scenes"][2]["asset_approved"]=False
    assert any("approved asset required" in e for e in validate_scene_plan(p))

def test_slow_hook_fails():
    p=good_plan()
    p["scenes"][0]["seconds"]=2
    assert "HOOK must finish within 1.5 seconds" in validate_scene_plan(p)

def test_publication_gate_cannot_open():
    p=good_plan()
    p["publication_gate"]="APPROVED"
    assert any("publication gate" in e for e in validate_scene_plan(p))
