from common import recv_image
from bg_subtraction import bg_subtraction
from my_image_subscriber import socket_setup
import numpy as np
import cv2 as cv
from constants import *
from utilities import *
from keras.models import load_model
from submission import submission
import time

model_file = MODEL_PATH + r"/model-118-0.0052.hdf5"
model = load_model(model_file)
reponse_payload = {
    "scene_no": 1,
    "ppe": {
        "helmet": False,
        "glasses": False,
        "coverall": False,
        "boots": False,
        "gloves": False
    }
}

def check_is_object(binary):
    r,c = binary.shape
    white = np.count_nonzero(binary)
    ratio = white/(r*c)
    return ratio >= 0.4

def object_detection(img):
    height, width, _ = img.shape
    
    lower_bound = {
        'helmet': 0,
        'glasses': 0,
        'coverall': int(height*0.15),
        'boots': int(height*0.75),
        'groove': int(height*0.25),
    }
    upper_bound = {
        'helmet': int(height*0.1),
        'glasses': int(height*0.1),
        'coverall': int(height*0.8),
        'boots': int(height),
        'groove': int(height*0.7),
    }
    

    result = img.copy()
    for k in lower_bound.keys():
        lower = lower_bound[k]
        upper = upper_bound[k]
        roi = img.copy()[:width, lower:upper]
        
        hsv = cv.cvtColor(roi.copy(), cv.COLOR_BGR2HSV)
        color_th = cv.inRange(hsv.copy(), COLOR_SEGMENT[k]['lower'], COLOR_SEGMENT[k]['upper'])
        is_obj = check_is_object(color_th)

        if is_obj:
            cv.rectangle(result, (0,lower), (width, upper), (255,255,0),-1)
            # update_payload()        
    

def color_detection(img):
    lower = [160, 0, 0]
    upper = [179, 255, 255]
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array(lower, np.uint8)
    upper = np.array(upper, np.uint8)


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
    print("prediction")
    rows, cols, ch = image.shape
    frame = image.copy()
    frame = cv.cvtColor(frame.copy(), cv.COLOR_BGR2RGB)
    frame = cv.resize(frame, (256, 256))
    frame = frame.reshape((1, 256, 256, 3))
    frame = frame.astype('float32')
    frame = (frame / 255.)
    pred = model.predict(frame)[0]

    pred = cv.resize(pred.copy(), (cols, rows))
    pred = cv.cvtColor(pred.copy(), cv.COLOR_RGB2BGR)
    pred = pred * 255.
    pred = pred.astype('uint8')
    return pred



def update_payload(name):
    global reponse_payload
    print("Update Payload")
    reponse_payload['ppe'][name] = True
    print(reponse_payload['ppe'][name])

def main():
    start_time = time.time()

    print("Socket initialize")
    socket = socket_setup()
    print("Socket setup successful")

    min_area = (FRAME_H * FRAME_W)*0.04
    get_bg = False

    while True:
        print("In loop")
        try:
            _, image = recv_image(socket)
            img = np.array(image)[:, :, ::-1]
            if img is None:
                print("Image is None")
                break
        except:
            print("Error exception")
            continue

        if not get_bg:
            print("Get Background")
            bg = img.copy()
            bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
            get_bg = True
            continue

        # fg = backSub.apply(frame)
        obj = bg_subtraction(img, bg.copy(), mode='neg')
        person = cv.bitwise_and(img, img, mask=obj)

        _, th = cv.threshold(obj, 127, 255, cv.THRESH_BINARY)
        th = cv.dilate(th, get_kernel())
        _, contours, _ = cv.findContours(
            th, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        result = img.copy()
        cv.drawContours(result, contours, -1, (255, 0, 0), 2)

        for cnt in contours:
            area = cv.contourArea(cnt)
            if area < min_area:
                continue
            (x, y, w, h) = cv.boundingRect(cnt)
            if w > FRAME_W * 0.3:
                print("Continues...")
                print("Width of object is too large")
                continue
            if h < FRAME_H*0.5:
                print("Continues...")
                print("Height of object is too short")
                continue
            if h/w < 1.5:
                print("Continues...")
                print("Height/Width Ratio is not ok")
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
            payload = object_detection(predicted)
            update_payload(payload)
            if time.time() - start_time > TIMEOUT:
                submission(reponse_payload,is_test=True)


        cv.imshow("obj", obj)
        cv.imshow("person", person)
        cv.imshow("result", result)
        k = cv.waitKey(1) & 0xff

        if k == ord('q'):
            break


if __name__ == "__main__":
    main()
