"""Cycle719 ten-genre proof-screen configuration. Full renderer in review ZIP."""
from dataclasses import dataclass
PALETTES={"ai_work":"#64D6FF","beauty":"#FF98D3","love_psychology":"#D6A7FF","saving":"#A9E781","sales_business":"#FFD07A","career":"#B4B1FF","health":"#80E9B5","science":"#52E7CF","travel_food":"#FFB987","product_comparison":"#83C6FF"}
WIDTH,HEIGHT,FPS=1080,1920,30
SCENE_START_FRAME,SCENE_FRAMES=118,59
@dataclass(frozen=True)
class ProofScreen:
 headline1:str="画面につなぐと、"
 headline2:str="操作できる。"
 label:str="03 / CONNECTION"
 code:str='print("Hello!")'
 output:str="Hello!"
 caption:str="画面につなぐと、操作できる。"
def validate(genre,slide):
 if genre not in PALETTES:raise ValueError("Unsupported genre")
 if not slide.headline1 or not slide.headline2 or not slide.caption:raise ValueError("Missing copy")
