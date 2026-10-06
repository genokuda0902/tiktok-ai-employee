import json
def test_cycle367_contract():
    p=json.load(open('quality_cycles/cycle367_contract.json',encoding='utf-8'))
    assert p['base_cycle']==366
    assert p['resolution']==[1080,1920]
    assert p['improvement_axis']=='nonaligned_scene_keep_vs_soften_quality_gate'
    assert all(x['action'] in ['KEEP','SOFTEN'] for x in p['decisions'])
    assert p['reusable_for_10_genres']
    assert not p['paid_service_used']
    assert not p['auto_post']
