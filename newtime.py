import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time

# 安康
bbox = [133, 550, 440, 585, 33]  # 安康码时间位置(:4)以及字体大小(-1)
img = cv2.imread("akm.jpg")
shp = (bbox[2] - bbox[0], bbox[3] - bbox[1])
im = Image.new("RGB", (bbox[2] - bbox[0], bbox[3] - bbox[1]), (254, 254, 254))
dr = ImageDraw.Draw(im)
font = ImageFont.truetype("arial.ttf", bbox[4])
dr.text((0, 0), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), (0, 0, 0), font)
img[bbox[1] : bbox[3], bbox[0] : bbox[2], :] = cv2.resize(np.array(im), shp)
cv2.imwrite("akm.jpg", img)

# 行程
bbox = [137, 238, 293, 258, 18]  # 行程码时间位置(:4)以及字体大小(-1)
color = (120, 120, 120)
img = cv2.imread("xcm.jpg")
shp = (bbox[2] - bbox[0], bbox[3] - bbox[1])
im = Image.new("RGB", (shp[0] + 20, shp[1]), (254, 254, 254))
dr = ImageDraw.Draw(im)
font = ImageFont.truetype("arial.ttf", bbox[4])

dr.text((0, 0), time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), color, font)
img[bbox[1] : bbox[3], bbox[0] : bbox[2], :] = cv2.resize(np.array(im), shp)
cv2.imwrite("xcm.jpg", img)
