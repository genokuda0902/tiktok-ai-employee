import json,subprocess,tempfile
from pathlib import Path
from reading_focus import POLICY,sha256,render,probe
with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp);src=p/'synthetic.mp4';out=p/'review.mp4';m=p/'manifest.json'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=#0d263e:s=1080x1920:r=30:d=5','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=5','-c:v','libx264','-threads','2','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-shortest',str(src)],check=True)
    m.write_text(json.dumps({'policy':POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,'source_sha256':sha256(src),'genre':'ai','layout_id':'writer_three_rows_v1','window':[1,3.5]}))
    report=render(src,out,m,p/'tmp')
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    assert probe(out)[1]==150,report
    print('SYNTHETIC AV QA PASS',report)
    from audio_chapter_audit import audit
    aud=audit(out,edges=(0,1,2,3,4,5))
    assert aud['all_chapters_have_audio'] and not aud['Japanese_transcript_verified']
    print('SYNTHETIC AUDIO CHAPTER QA PASS')
