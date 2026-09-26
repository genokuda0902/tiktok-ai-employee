"""Structured creative candidates and safe feedback adapter, not a generative model."""
from datetime import datetime, timezone
from video_engine.production_v2.integration import load_feedback

NEGATIVE = ('readable text','watermark','social platform UI','unauthorized logo','unauthorized likeness','extra fingers','malformed hands','distorted face','flicker','broken physics','random symbols','inconsistent objects')
STYLES = {
 'A':('リアル系AI違和感','office realism with one impossible change','result-first visual contradiction'),
 'B':('ミニチュアAI仕事場','miniature helpers processing a life-size task','tiny worker reveals oversized result'),
 'C':('Before / After ＋ Loop','mess to organized result and seamless loop','before/after in the first second'),
}

def candidates(theme, target, trace_id, video_id, feedback=None):
    if not theme or not target or not trace_id or not video_id: raise ValueError('Theme and identifiers required')
    out=[]
    for label,(title,visual_style,hook) in STYLES.items():
        c={'variant':label,'video_id':video_id,'trace_id':trace_id,'theme':theme,'title':theme+' / '+title,'one_sentence_concept':visual_style,'target':target,'purpose':'compare retention and meaningful engagement, without performance guarantees','hook_options':[hook,'result first','visual comparison','one surprising detail','question about the result'],'duration_seconds':20,'cut_count':8,'cta':'Save or comment if useful','comparison_controls':{'theme':theme,'duration_seconds':20,'cta':'Save or comment if useful','keywords':[theme]},'variable':{'visual_style':visual_style,'hook':hook,'audio_mood':label},'risk':['fiction and estimates must be disclosed','human visual and rights review required'],'created_at':datetime.now(timezone.utc).isoformat(),'negative_prompt':list(NEGATIVE),'character_reference_id':None,'scene_prompts':[]}
        for i in range(8):
            prompt={'subject':theme,'environment':'office or daily life','camera_position':'eye level','lens':'35mm natural perspective','camera_motion':'subtle push in','lighting':'soft natural light','color':'high contrast legible','texture':'photographic','single_action':'one visible change','continuity':{'person':c['character_reference_id'],'outfit':'consistent','background':'consistent','props':'consistent','palette':'consistent'},'next_scene_connection':'match action cut','no_text_generated':True}
            c['scene_prompts'].append({'scene_id':i+1,'start_time':i*2.5,'end_time':(i+1)*2.5,'duration':2.5,'purpose':'hook' if i==0 else 'one visual beat','visual':visual_style,'camera':'eye level','motion':'subtle push in','narration':'Draft pending TTS','caption':'Draft pending edit','sound_effect':'short only when action warrants','asset_type':'ai_image_or_video','asset_id':None,'visual_prompt':prompt,'negative_prompt':list(NEGATIVE),'rights_status':'PENDING','quality_risk':['face, hands, props, continuity'],'transition':'cut'})
        out.append(c)
    if feedback:
        if feedback['video_id']!=video_id or feedback['trace_id']!=trace_id: raise ValueError('Feedback trace mismatch')
        for c in out:c['prior_feedback']=feedback
    return out
