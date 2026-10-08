"""Register an AI image or licensed media for a scene; never invent a rights grant."""
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

ALLOWED={'ai_image','self_shot','licensed_image','screen_recording','licensed_video','ai_video'}

def register(path,asset_id,asset_type,source,rights_basis,rights_evidence,visual_prompt=None,generated_at=None,model=None,privacy_review='pending'):
    file=Path(path).resolve(strict=True)
    if asset_type not in ALLOWED or not asset_id or not source or not rights_basis or not rights_evidence:raise ValueError('Source and rights assertions required')
    if asset_type.startswith('ai_') and (not visual_prompt or not model or not generated_at):raise ValueError('AI generation provenance required')
    if asset_type.endswith('image') or asset_type=='self_shot':
        with Image.open(file) as im:width,height=im.size
        if width*16!=height*9 or width<1080 or height<1920:raise ValueError('1080x1920 or larger 9:16 original required')
        media_type='image'
    else:media_type='video' # PR #21 renderer independently checks video dimensions/length.
    return {'asset_id':asset_id,'path':str(file),'type':media_type,'source_type':asset_type,'source':source,'rights_basis':rights_basis,'rights_evidence':rights_evidence,'commercial_use':False,'derivatives_allowed':False,'privacy_review':privacy_review,'ai_generated':asset_type.startswith('ai_'),'ai_disclosure':asset_type.startswith('ai_'),'visual_prompt':visual_prompt,'generation_model':model,'generated_at':generated_at,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'publication_approved':False}


def validate_for_render(asset):
    """Fail closed before an asset enters the renderer."""
    required=('path','sha256','rights_evidence','privacy_review','publication_approved')
    if any(k not in asset for k in required):
        raise ValueError('Incomplete asset approval metadata')
    if asset['privacy_review'] != 'approved':
        raise ValueError('Privacy review approval required')
    if asset['publication_approved'] is not True:
        raise ValueError('Publication approval required')
    if not asset['rights_evidence']:
        raise ValueError('Rights evidence required')
    file=Path(asset['path']).resolve(strict=True)
    actual=hashlib.sha256(file.read_bytes()).hexdigest()
    if actual != asset['sha256']:
        raise ValueError('Asset checksum changed after approval')
    return asset
