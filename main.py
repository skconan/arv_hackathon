from common import recv_image
from bg_subtraction import bg_subtraction
from my_image_subscriber import socket_setup
import numpy as np
import cv2 as cv


def main():
    socket = socket_setup()
    while True:
        # print("Try to get background")
        # meta_data, image = recv_image(socket)
        # img = np.array(image)[:,:,::-1]
        # if img is None:
        #     continue
        try:
            print("Try to get background")
            meta_data, image = recv_image(socket)
            img = np.array(image)[:, :, ::-1]
            if img is None:
                continue
        except:
            continue

        bg = img.copy()
        cv.imshow("background", bg)
        k = cv.waitKey(-1) & 0xff
        if k == ord('q'):
            break
        else:
            continue
    bg = cv.cvtColor(bg.copy(), cv.COLOR_BGR2GRAY)
    print("Get bg success")
    while True:
        try:
            meta_data, image = recv_image(socket)
            img = np.array(image)[:, :, ::-1]
            if img is None:
                continue

        except:
            continue
        cv.imshow("img", img)
        obj = bg_subtraction(img, bg)
        # obj1 = bg_subtraction(img, bg, 'pos')
        person = cv.bitwise_and(img, img, mask=obj)
        cv.imshow("obj", obj)
        cv.imshow("person", person)
        # cv.imshow("obj1", obj1)
        k = cv.waitKey(1) & 0xff
        if k == ord('q'):
            break


if __name__ == "__main__":
    main()
