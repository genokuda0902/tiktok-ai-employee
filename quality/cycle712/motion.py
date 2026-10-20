"""Reusable proof-graph animation logic for ten content genres."""

def reveal_count(frame_index:int,frame_count:int=90,item_count:int=4)->int:
    if type(frame_index) is not int or type(frame_count) is not int or type(item_count) is not int:
        raise ValueError('integer frame and item counts required')
    if frame_count<item_count or item_count<1 or not 0<=frame_index<frame_count:
        raise ValueError('invalid animation frame')
    return min(item_count,1+(frame_index*item_count)//frame_count)

def verified_bars(values):
    if not values or any(type(v) is not int or v<0 for v in values):
        raise ValueError('nonnegative integer source values required')
    return tuple(values)
