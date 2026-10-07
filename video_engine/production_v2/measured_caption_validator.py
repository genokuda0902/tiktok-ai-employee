"""Fail-closed measured-caption contract; human review still required."""
import math
def validate_measured_caption_timeline(scenes, measured, source):
    if source != 'measured_aivis_scene_duration':
        raise ValueError('Untrusted measured caption timing source')
    if not isinstance(measured,list) or len(measured)!=len(scenes):
        raise ValueError('Measured caption timeline scene count mismatch')
    out=[]; prev=0.0
    for scene,item in zip(scenes,measured):
        if not isinstance(item,dict): raise ValueError('Invalid measured caption timeline item')
        sid=scene.get('scene_id',scene.get('id'))
        if not sid or item.get('scene_id')!=sid:
            raise ValueError('Measured caption timeline scene ID mismatch')
        if item.get('text')!=scene.get('caption'):
            raise ValueError('Measured caption text mismatch')
        try:
            a,b,d=float(item['start']),float(item['end']),float(scene['duration'])
        except (KeyError,ValueError,TypeError,OverflowError):
            raise ValueError('Invalid measured caption timestamp') from None
        if not all(map(math.isfinite,(a,b,d))):
            raise ValueError('Invalid measured caption timestamp')
        if abs(a-prev)>0.02: raise ValueError('Measured caption timeline gap/overlap')
        if b<=a or d<=0 or abs(b-a-d)>0.02:
            raise ValueError('Measured caption duration mismatch')
        out.append({'text':item['text'],'start':a,'end':b});prev=b
    if abs(prev-sum(float(s['duration']) for s in scenes))>0.02:
        raise ValueError('Measured caption total duration mismatch')
    return out
