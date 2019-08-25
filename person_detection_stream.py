from common import recv_image
from bg_subtraction import bg_subtraction
from my_image_subscriber import socket_setup
import numpy as np
import cv2 as cv
from constants import *
from utilities import *
from keras.models import load_model

model_file = MODEL_PATH + r"/model-color-obj-bg.hdf5"
model = load_model(model_file)

def object_detection(img):
    height, width, _ = img.shape
    check = {
             'helmet':False,
             'coverall':False,
             'boots':False,
             'groove':False,
             }
    
    lower_bound = {
        'helmet': 0,
        'coverall': int(height*0.15),
        'boots': int(height*0.75),
        'groove': int(height*0.25),
    }
    upper_bound = {
        'helmet': int(height*0.1),
        'coverall': int(height*0.8),
        'boots': int(height),
        'groove': int(height*0.7),
    }
    color = {
        'helmet': {
          'lower': np.array([127,127,127],np.uint8),
          'upper': np.array([255,255,255],np.uint8)
        },
        'coverall': {
          'lower': np.array([127,127,127],np.uint8),
          'upper': np.array([255,255,255],np.uint8)
        },
        'boots': (255, 0, 0),
        'groove': (0, 255, 0),
    }

    # helmet = img.copy()[:,:]
    result = img.copy()
    for k in lower_bound.keys():
        lower = lower_bound[k]
        upper = upper_bound[k]
        # cv.rectangle(result, (0, lower), (width, upper), color[k], 2)
        roi = img.copy()[:width,lower:upper]
        hsv = cv.cvtColor(roi.copy(),cv.COLOR_BGR2HSV)
        color_th = cv.inRange(hsv.copy(), lower)
    cv.imshow('result_divide', result)
    cv.waitKey(1)


def color_detection(img):
    lower = [160,0,0]
    upper = [179, 255,255]
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array(lower,np.uint8)
    upper = np.array(upper,np.uint8)

def capture():
    name = "out.avi"
    cap = cv.VideoCapture(VDO_PATH + "/" + name)
    while True:
        ret, img = cap.read()
        if ret:
            cv.imwrite(IMG_PATH + "/bg.jpg", img)
            break



def predict(image):
    global model
    rows,cols,ch = image.shape
    frame = image.copy()
    frame = cv.cvtColor(frame.copy(), cv.COLOR_BGR2RGB)
    frame = cv.resize(frame,(256,256))
    frame = frame.reshape((1,256,256,3))
    frame = frame.astype('float32')
    frame = (frame / 255.)
    pred = model.predict(frame)[0]
        
    pred = cv.resize(pred.copy(), (cols,rows))	
    pred = cv.cvtColor(pred.copy(), cv.COLOR_RGB2BGR)
    pred = pred * 255.
    pred = pred.astype('uint8')
    return pred

def main():
    vdo_path = r"D:\hackathon\hackathon_image_streaming\videos"
    # bg = cv.imread(IMG_PATH + "/bg.jpg",0)
    # bg = cv.GaussianBlur(bg, (11, 11), 0)
    name = "out_all_forward.avi"
    name = "out_all_no_hand.avi"
    # vdo_name = 
    # cap = cv.VideoCapture()
    cap = cv.VideoCapture(VDO_PATH + "/" + name)
    min_area = (FRAME_H * FRAME_W)*0.04
    # back_sub = cv.createBackgroundSubtractorKNN()
    get_bg = False
    frame_count = 0
    while True:
        try:
            ret, img = cap.read()
            if not ret:
                print("Image is None")
                break
        except:
            continue
        if not get_bg:
            bg = img.copy()
            bg = cv.cvtColor(bg,cv.COLOR_BGR2GRAY)
            get_bg = True
            continue
        
        # fg = backSub.apply(frame)
        obj = bg_subtraction(img, bg.copy(), mode='neg')
        person = cv.bitwise_and(img, img, mask=obj)

        _,th = cv.threshold(obj, 127, 255, cv.THRESH_BINARY)
        # th = cv.erode(th,get_kernel(ksize=(5,5)))
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
            if w > FRAME_W * 0.3:
                continue
            if h < FRAME_H*0.5:
                continue
            if h/w < 1.5:
                continue
            # wh_ratio = 1.*w/h
            add_h = h*0.25
            y = max(0, y-add_h)
            h = min(FRAME_H, h+add_h)
            y = int(y)
            h = int(h)
            cv.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = img[y:y+h, x:x+w]
            predicted = predict(roi)
        frame_count += 1
        # if frame_count >= 30:
        #     frame_count = 0
        #     get_bg = False
        cv.imshow("obj", obj)
        # cv.imshow("img", img)
        # cv.imshow("bg", bg)
        cv.imshow("person", person)
        cv.imshow("result", result)
        k = cv.waitKey(100) & 0xff
        if k == ord('q'):
            break
    cap.release()

if __name__ == "__main__":
    main()