import numpy as np
WS_PATH = r"D:\hackathon\hackathon_image_streaming"
VDO_PATH = WS_PATH + r"\videos"
MODEL_PATH = WS_PATH + r"\models"
IMG_PATH = WS_PATH + r"\images"
PERSON_PATH = WS_PATH + r"\person"
FRAME_W = 640
FRAME_H = 480
COLOR_SEGMENT = {
    'helmet': {
        'upper': np.array([38, 255, 255], np.uint8), 'lower': np.array([22, 0, 0], np.uint8)
    },

    'grasses':
    {
        'upper': np.array([130, 255, 255], np.uint8), 'lower': np.array([75, 0, 0], np.uint8)
    },
    'groove':
    {
        'upper': np.array([75, 255, 255], np.uint8), 'lower': np.array([38, 0, 0], np.uint8)
    },
    'boots': {

        # Boot
        'upper': np.array([179, 255, 255], np.uint8), 'lower': np.array([160, 0, 0], np.uint8)

    },

    'coverall': {

        'upper': np.array([160, 255, 255], np.uint8), 'lower': np.array([130, 0, 0], np.uint8)
    }
}
