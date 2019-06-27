# we can calculate Distance of object: D' = (F * W)/P

import numpy as np
import cv2
import stop_sign_detection
#from focal_length import calculate_focal_length

def calculate_focal_length():
    # using camera from webcam LAB
    w = 5.5
    p = 211
    d =  40 
    f = ((p * d) / w)
    return [f, w]

def distance(frame, stop_coor):
    x = calculate_focal_length()
    f = x[0]
    w = x[1]
    if type(stop_coor) == tuple:
        stop_coor
    elif type(stop_coor) == np.ndarray:
        p = stop_coor[0, 2]
        d = int(((w) * f / p))
        print('distance:',d)
        cv2.putText(frame, 'distance object: ' + str(d) + 'cm', (100, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))

def main_video():
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        ret, frame = cap.read()

        stop_coor = stop_sign_detection.stop(frame) 
        #print(stop_coor)

        distance(frame, stop_coor)

        cv2.imshow('xxx', frame)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()
    cap.release
