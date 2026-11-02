"""Only synthetic fictional media; no private MP4 in CI."""
import hashlib,json,subprocess,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import proof_chart as p
with tempfile.TemporaryDirectory() as d:
    d=Path(d);src=d/'synthetic.mp4';out=d/'out.mp4';m=d/'m.json';r=d/'report.json'
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x071425:s=1080x1920:r=30:d=3',
      '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=3','-shortest',
      '-c:v','libx264','-threads','2','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac',str(src)],check=True)
    data={'policy':p.POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,
      'roi_reviewed':True,'genre':'ai','source_sha256':p.digest(src),'roi':[54,806,940,240],
      'time':[.2,2.8],'fictional_data':{'A':[12,16,18],'B':[8,9,12]}}
    m.write_text(json.dumps(data),encoding='utf-8')
    res=p.render(src,out,m,r)
    assert res['technical_pass'] and res['fictional_totals']['total']==75
    print('SYNTHETIC ONLY PASS',out.stat().st_size)
