from common import recv_image
from bg_subtraction import bg_subtraction
from my_image_subscriber import socket_setup
import numpy as np
import cv2 as cv
from constants import *
from utilities import *

def capture():
    name = "out.avi"
    cap = cv.VideoCapture(VDO_PATH + "/" + name)
    while True:
        ret, img = cap.read()
        if ret:
            cv.imwrite(IMG_PATH + "/bg.jpg", img)
            break
def main():
    vdo_path = r"D:\hackathon\hackathon_image_streaming\videos"
    bg = cv.imread(IMG_PATH + "/bg.jpg",0)
    name = "out_all_forward.avi"
    # vdo_name = 
    # cap = cv.VideoCapture()
    cap = cv.VideoCapture(VDO_PATH + "/" + name)
    min_area = (FRAME_H * FRAME_W)*0.04
    # back_sub = cv.createBackgroundSubtractorKNN()
    while True:
        try:
            ret, img = cap.read()
            if not ret:
                print("Image is None")
                break
        except:
            continue

        # fg = backSub.apply(frame)
        obj = bg_subtraction(img, bg.copy(), mode='neg')
        person = cv.bitwise_and(img, img, mask=obj)

        _,th = cv.threshold(obj, 127, 255, cv.THRESH_BINARY)
        th = cv.dilate(th,get_kernel())
        cv.imshow("th",th)
        _,contours,_ = cv.findContours(th,cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        frame_move = 0
        result = img.copy()
        cv.drawContours(result,contours,-1,(255,0,0),2)
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area < min_area:
                continue
            (x, y, w, h) = cv.boundingRect(cnt)
            cv.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)  

        cv.imshow("obj", obj)
        # cv.imshow("img", img)
        cv.imshow("bg", bg)
        cv.imshow("person", person)
        cv.imshow("result", result)
        k = cv.waitKey(100) & 0xff
        if k == ord('q'):
            break
    cap.release()

if __name__ == "__main__":
    main()