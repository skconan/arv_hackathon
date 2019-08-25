import numpy as np
WS_PATH = r"D:\hackathon\hackathon_image_streaming"
VDO_PATH = WS_PATH + r"\videos"
MODEL_PATH = WS_PATH + r"\models"
IMG_PATH = WS_PATH + r"\images"
PERSON_PATH = WS_PATH + r"\person"
FRAME_W = 640
FRAME_H = 480
TIMEOUT = 25
COLOR_SEGMENT = {
    'helmet': {
        'upper': np.array([38, 255, 255], np.uint8), 'lower': np.array([20, 220, 0], np.uint8)
    },

    'glasses':
    {
        'upper': np.array([130, 255, 255], np.uint8), 'lower': np.array([75, 0, 0], np.uint8)
    },
    'groove':
    {
        'upper': np.array([80, 255, 255], np.uint8), 'lower': np.array([50, 220, 0], np.uint8)
    },
    'boots': {
        'upper': np.array([25, 255, 255], np.uint8), 'lower': np.array([0, 220, 0], np.uint8)

    },

    'coverall': {
        'upper': np.array([155, 255, 255], np.uint8), 'lower': np.array([135, 220, 0], np.uint8)
    }
}
