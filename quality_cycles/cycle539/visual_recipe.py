"""Cycle539 reusable original illustration geometry (review only)."""
import numpy as np
import cv2
from PIL import Image

GENRES = ('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')

def warp_subject(rgb, corners, out_size=(1080,780)):
    h,w=rgb.shape[:2]
    src=np.float32([[0,0],[w-1,0],[w-1,h-1],[0,h-1]])
    transform=cv2.getPerspectiveTransform(src,np.float32(corners))
    img=cv2.warpPerspective(rgb,transform,out_size)
    mask=cv2.warpPerspective(np.full((h,w),255,np.uint8),transform,out_size)
    return Image.fromarray(np.dstack([img,mask]),'RGBA')

def feathered_zone(width=1080,height=835,border=20,sigma=15):
    alpha=np.zeros((height,width),np.float32)
    alpha[border:-border,:]=1
    return cv2.GaussianBlur(alpha,(0,0),sigmaX=sigma,sigmaY=sigma)
