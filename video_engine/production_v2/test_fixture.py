"""Create wholly synthetic and unapproved 20-second fixture. Tone is not Japanese speech."""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image,ImageDraw

def create(folder):
    p=Path(folder).resolve();p.mkdir(parents=True,exist_ok=True)
    colors=['#172554','#064e3b','#713f12','#581c87','#7f1d1d','#164e63','#365314','#1e293b']
    assets={}; scenes=[]
    for i,color in enumerate(colors,1):
        im=Image.new('RGB',(1080,1920),color); d=ImageDraw.Draw(im)
        d.rounded_rectangle((110,370,970,1390),radius=100,fill='#ffffff',outline='#94a3b8',width=10)
        d.ellipse((270+i*23,620,600+i*23,950),fill=color)
        path=f'scene_{i:02}.png';im.save(p/path)
        key=f'asset_{i:02}'
        assets[key]={'path':path,'type':'image','source_type':'synthetic_test','rights_basis':'created in test job','rights_evidence':'test_fixture.py','commercial_use':False,'derivatives_allowed':False,'privacy_review':'synthetic','ai_generated':False,'generated_at':datetime.now(timezone.utc).isoformat()}
        scenes.append({'scene_id':i,'duration':2.5,'purpose':('hook' if i==1 else 'demonstration'),'visual_prompt':'synthetic geometric test card','asset_type':'image','asset_id':key,'narration':'TEST TONE ONLY','caption':'連携テスト・公開禁止','motion':('zoom_in' if i%2 else 'static'),'transition':'cut','rights_status':'TEST_ONLY'})
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','sine=frequency=440:duration=20','-ar','48000',str(p/'tone.wav')],check=True)
    plan={'video_id':'video_e2e_test_0001','plan_id':'plan_e2e_test_0001','genre':'workflow_test','title':'未承認の連携テスト','target_audience':'internal test','audience_problem':'verify end-to-end artifact','hook_first_3s':'連携テスト・公開禁止','structure':'synthetic eight-scene test','narration':'No narration; test tone only','narration_file':'tone.wav','captions':'連携テスト・公開禁止','required_assets':list(assets),'cta':'none','risks':['test tone not Japanese speech','no publication rights clearance'],'sources':['locally generated fixture'],'expected_seconds':20,'created_at':datetime.now(timezone.utc).isoformat(),'version':1,'publication_status':'UNAPPROVED_TEST','assets':assets,'scenes':scenes,'revision_history':[]}
    (p/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
    return p/'plan.json'
if __name__=='__main__':
    import sys
    print(create(sys.argv[1]))
