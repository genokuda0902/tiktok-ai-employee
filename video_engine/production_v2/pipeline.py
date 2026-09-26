"""Review-only production orchestration around PR #21's renderer."""
import argparse
import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from video_engine.portrait_v2.build import main as render, probe

CATEGORIES = ('structure', 'legibility', 'audio', 'content', 'rights', 'tiktok_quality')
ALLOWED = {'caption', 'visual_prompt', 'asset_id', 'motion', 'narration'}

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')

def request_revision(plan, request, authorized_subject):
    required = ('video_id', 'requested_by', 'requested_at', 'scene_id', 'change_type', 'instruction', 'previous_version', 'new_version', 'status')
    if any(k not in request for k in required): raise ValueError('Incomplete revision request')
    if not authorized_subject or request['requested_by'] != authorized_subject: raise PermissionError('Trusted authentication required')
    if request['video_id'] != plan['video_id'] or request['previous_version'] != plan['version'] or request['new_version'] != plan['version'] + 1: raise ValueError('Stale or foreign video revision')
    if request['change_type'] not in ALLOWED or request['status'] != 'REQUESTED': raise ValueError('Unsupported revision')
    match = [s for s in plan['scenes'] if s['scene_id'] == request['scene_id']]
    if len(match) != 1: raise ValueError('Scene not found')
    revised = copy.deepcopy(plan)
    target = next(s for s in revised['scenes'] if s['scene_id'] == request['scene_id'])
    # Free-form instructions are recorded only; never executed as code or substituted
    # for an asset or fact. An editor must supply a validated proposed_value.
    if request['change_type'] in ('asset_id', 'motion', 'caption', 'narration'):
        value = request.get('proposed_value')
        if not isinstance(value, str) or not value.strip(): raise ValueError('Validated proposed_value required')
        if request['change_type'] == 'asset_id' and value not in plan['assets']: raise ValueError('Unknown asset')
        if request['change_type'] == 'motion' and value not in ('static','zoom_in','zoom_out','pan_left','pan_right'): raise ValueError('Unknown motion')
        target[request['change_type']] = value
    else:
        target['visual_prompt'] = request['instruction']
        target['asset_id'] = None  # Changed visual must be supplied before rendering.
    revised['version'] += 1
    revised.setdefault('revision_history', []).append({**request, 'status':'APPLIED_FOR_REVIEW'})
    return revised

def produce(plan_path, output_root):
    plan_path = Path(plan_path).resolve(); plan = json.loads(plan_path.read_text(encoding='utf8'))
    if plan.get('publication_status') != 'UNAPPROVED_TEST': raise ValueError('Only unapproved integration test plans are accepted')
    scenes = plan['scenes']; assets = plan['assets']
    if not 6 <= len(scenes) <= 10 or len({s['scene_id'] for s in scenes}) != len(scenes): raise ValueError('Invalid scenes')
    required_plan = ('plan_id','genre','title','target_audience','audience_problem','hook_first_3s','structure','narration','captions','required_assets','cta','risks','sources','expected_seconds','created_at','version')
    if any(k not in plan for k in required_plan): raise ValueError('Incomplete plan')
    required_scene = ('scene_id','duration','purpose','visual_prompt','asset_type','asset_id','narration','caption','motion','transition','rights_status')
    if any(any(k not in scene for k in required_scene) for scene in scenes): raise ValueError('Incomplete scene')
    total = sum(float(s['duration']) for s in scenes)
    if not 15 <= total <= 25: raise ValueError('Expected 15–25 seconds')
    dest = Path(output_root).resolve() / f"{plan['video_id']}_v{plan['version']}"
    if dest.exists(): raise FileExistsError('Version is immutable')
    dest.mkdir(parents=True)
    write(dest/'plan.json', plan)
    captions = []; cursor = 0
    for scene in scenes:
        captions.append({'text':scene['caption'], 'start':cursor, 'end':cursor+float(scene['duration'])})
        cursor += float(scene['duration'])
    write(dest/'captions.json', captions)
    write(dest/'rights.json', {k:{field:value for field,value in asset.items() if field != 'path'} for k,asset in assets.items()})
    write(dest/'revision_history.json', plan.get('revision_history', []))
    narration_file=(plan_path.parent/plan['narration_file']).resolve()
    if plan.get('soundtrack'):
        from video_engine.production_v2.sound import mix
        sound=plan['soundtrack']
        mix(narration_file,(plan_path.parent/sound['bgm']).resolve(),(plan_path.parent/sound['sfx']).resolve(),dest/'mix.wav',total,sound['rights'])
        narration_file=dest/'mix.wav'
    # Resolve media relative to the source plan, not the generated output directory.
    media = {k:{**asset,'path':str((plan_path.parent/asset['path']).resolve())} for k,asset in assets.items()}
    config = {'mode':'technical_test','output':'video.mp4','narration':str(narration_file),'captions':'captions.json','assets':media,'scenes':[{'asset_id':s['asset_id'],'seconds':s['duration'],'motion':s['motion']} for s in scenes]}
    write(dest/'render_config.json', config)
    checks = {k:[] for k in CATEGORIES}
    checks['structure'].append({'check':'scene_count', 'passed':6<=len(scenes)<=10})
    checks['legibility'].append({'check':'caption_length', 'passed':all(0<len(s['caption'])<=28 for s in scenes)})
    checks['content'].append({'check':'sources_provided', 'passed':bool(plan['sources'])})
    checks['legibility'].append({'check':'caption_safe_zone_visual', 'passed':None, 'reason':'ASS bottom margin 410px; phone frame review pending'})
    checks['tiktok_quality'].append({'check':'first_1_5_seconds_visual_hook', 'passed':None, 'reason':'visual impact requires human review'})
    checks['audio'].append({'check':'separate_voice_bgm_sfx', 'passed':bool(plan.get('soundtrack')), 'reason':'Absent tracks require human review' if not plan.get('soundtrack') else 'mix metadata recorded'})
    checks['rights'].append({'check':'human_rights_clearance', 'passed':False, 'reason':'UNAPPROVED_TEST'})
    checks['tiktok_quality'].append({'check':'human_phone_review', 'passed':False})
    try:
        render(dest/'render_config.json')
        video=dest/'video.mp4'; data=probe(video)
        write(dest/'ffprobe.json',data)
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],check=True)
        streams=data['streams']; v=next(s for s in streams if s['codec_type']=='video')
        checks['structure'].append({'check':'resolution_duration_decode', 'passed':(v['width'],v['height'])==(1080,1920) and 14.8<=float(data['format']['duration'])<=25.2})
        checks['audio'].append({'check':'audio_track', 'passed':any(s['codec_type']=='audio' for s in streams)})
        checks['audio'].append({'check':'human_japanese_pronunciation', 'passed':False})
        digest=hashlib.sha256(video.read_bytes()).hexdigest()
        (dest/'SHA256SUMS').write_text(f'{digest}  video.mp4\n')
        result='REGENERATE' if any(c['passed'] is False for cat in ('structure','legibility') for c in checks[cat]) else 'HUMAN_REVIEW'
    except Exception as exc:
        checks['structure'].append({'check':'render', 'passed':False,'reason':str(exc)[-500:]})
        result='REGENERATE'; digest=None
    write(dest/'qa.json',{'categories':checks,'result':result,'quality_status':'QUALITY_NOT_APPROVED','publication_status':'NOT_APPROVED','sha256':digest,'generated_at':datetime.now(timezone.utc).isoformat()})
    if digest is None: raise RuntimeError(f'Render or decode failed; see {dest}/qa.json')
    print(json.dumps({'path':str(dest),'sha256':digest,'qa':result}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('plan');parser.add_argument('out');args=parser.parse_args();produce(args.plan,args.out)
