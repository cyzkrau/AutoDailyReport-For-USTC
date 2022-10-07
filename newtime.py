import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time

def create(number):
    img = cv2.imread("xcm.jpg")

    im = Image.new("RGB", (805, 100), (254, 254, 254))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("heiti.ttf", 58)
    text = time.strftime("更新于：%Y.%m.%d %H:%M:%S",time.localtime(time.time()+8*3600-30))
    dr.text((30, 0), text, (120, 120, 120), font)
    img[545: 645, 180: 985, :] = np.array(im)

    im = Image.new("RGB", (805, 100), (254, 254, 254))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("heiti.ttf", 50)
    text = str(number) + "的动态行程卡"
    dr.text((115, 0), text, (0, 0, 0), font)
    img[427: 527, 180: 985, :] = np.array(im)

    cv2.imwrite("xcm.jpg", img)
