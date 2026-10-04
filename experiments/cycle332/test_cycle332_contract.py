import json
p=json.load(open('experiments/cycle332/cycle332_contract.json',encoding='utf-8'))
assert p['base_cycle']==331
assert p['resolution']==[1080,1920]
assert p['improvement_axis']=='dual_ui_safezone_plus_progress_rail'
s=p['safe_zones']['subtitle']
assert s['x']+s['w']<=850
assert s['y']+s['h']<=1515
assert p['progress_rail']['steps']==6
assert p['paid_service_used'] is False and p['auto_post'] is False
print('PASS: cycle332 dual-safezone/progress contract')
