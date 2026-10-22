from prompt_timeline import validate_review_manifest

BASE = dict(genre='AI・仕事効率化', status='HUMAN_REVIEW', post_policy='employee_manual_after_approval', asset_origin='original_synthetic_pillow', synthetic_data=True, sales=[120000,150000,200000,180000])

def test_review_gate():
    validate_review_manifest(BASE)
    for key,value in [('status','APPROVED'),('post_policy','automatic'),('asset_origin','unlicensed'),('synthetic_data',False)]:
        bad = dict(BASE)
        bad[key] = value
        try:
            validate_review_manifest(bad)
        except ValueError:
            continue
        raise AssertionError(key)
