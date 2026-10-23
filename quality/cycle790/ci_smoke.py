"""CI-only 3-second synthetic-tone fixture; NOT the user's complete Japanese video."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from repair_wipe import render

def main(source,output):
    source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    cfg={'mode':'review_only','rights_reviewed':False,'publication_approved':False,
         'canvas':[1080,1920],'fps':30,'genre':'synthetic_ci_only',
         'fixes':[{'first_frame':35,'last_frame':50,'before_at':0.8,'after_at':2.3}]}
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'config.json';p.write_text(json.dumps(cfg))
        report=Path(td)/'report.json'
        result=render(source,output,p,report)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True)
    result['not_full_user_video']=True
    result['not_japanese_speech']=True
    result['synthetic_tone_only']=True
    output.with_suffix('.json').write_text(json.dumps(result,indent=2))
    return result
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--input',required=True);a.add_argument('--output',required=True)
    args=a.parse_args();print(json.dumps(main(args.input,args.output)))
