import cv2 as cv
import numpy as np

def normalize(gray):
    a = (gray.max()-gray.min()) + 1
    return np.uint8(255*(gray-gray.min())/a)

def bg_subtraction(fg, bg, bg_k=1, fg_k=3, mode='neg'):
    # hsv = cv.cvtColor(fg, cv.COLOR_BGR2HSV)
    # gray,_,_ = cv.split(hsv)
    fg = cv.cvtColor(fg.copy(),cv.COLOR_BGR2GRAY)

    # start_time = rospy.Time.now()
    # bg = cv.medianBlur(bg.copy(), 15)
    # fg = cv.medianBlur(fg.copy(), 7)
    # fg = kmean(gray, k=fg_k)
 

    sub_sign = np.int16(fg) - np.int16(bg)
    
    if mode == 'neg':
        sub_neg = np.clip(sub_sign.copy(),sub_sign.copy().min(),0)
        sub_neg = normalize(sub_neg)
        _, result = cv.threshold(
            sub_neg, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU
        )
        cv.imshow("sub_neg",sub_neg.copy())
        # _, result = cv.threshold(
        #     sub_neg, 127, 255, cv.THRESH_BINARY
        # )
    elif mode == 'pos':
        sub_pos = np.clip(sub_sign.copy(),0,sub_sign.copy().max())
        sub_pos = normalize(sub_pos)
        _, result = cv.threshold(
            sub_pos, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU
        )
    else:
        # sub = np.absolute(sub_sign.copy())
        # sub = normalize(sub)
        sub = cv.absdiff(bg, fg)
        # _, result = cv.threshold(
        #     sub, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU
        # )
        # _, result = cv.threshold(
        #     sub, 25, 255, cv.THRESH_BINARY
        # )
    # cv.imshow("sub_neg",sub.copy())
    # time_duration = rospy.Time.now()-start_time
    # print(time_duration.to_sec())
    # cv.imshow("fg",fg)
    # cv.imshow("bg",bg)

    return result

