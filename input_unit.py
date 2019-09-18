import urllib.request
import cv2
import numpy as np
import tracking_lanes
from tracking_lanes.tracking_lanes_2 import line_detection, edge_detection, region_of_interest
import time
from .self_driving.self_driving import prediction

root_url = "http://192.168.1.8/"

def sendRequest(url):
    n = urllib.request.urlopen(url)  # send request to ESP

def command(c):
    if c == 1:
        sendRequest(root_url+"/forward")
    elif c == 2:
        sendRequest(root_url+"/right")
    elif c == 3:
        sendRequest(root_url+"/left")
    elif c == 0:
        sendRequest(root_url+"/stop")

if __name__ == '__main__':
    last_time = time.time()
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        image = np.copy(frame)
        
        # PROCESS IMAGE
        edge_image = edge_detection(image)
        roi_image = region_of_interest(edge_image)
        processed_image, c = line_detection(image)

        # SHOW COMMAND
        #print('command is ', c)
        command(c)

        # DISPLAY PROCESSED IMAGE
        #cv2.imshow('original', frame)
        #cv2.imshow('edge', edge_image)
        #cv2.imshow('roi', roi_image)
        cv2.imshow('xxx', processed_image)

        #print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()

        if cv2.waitKey(10) & 0xFF == ord('x'):
            sendRequest(root_url+"/exit")
            cv2.destroyAllWindows()
            cap.release()

    # image = cv2.imread(r"C:\Users\DucTRung\Documents\OpenCV\finding-lanes\Picture_test\image_test.jpg")
    # img = np.copy(image)
    # # (h, w) = image.shape[:2]
    # # center = (w // 2, h // 2)
    # # M = cv2.getRotationMatrix2D(center, 270, 1)
    # # img = cv2.warpAffine(image, M, (h, w))

    # edge_img = edge_detection(img)
    # roi_img = region_of_interest(edge_img)
    # processed_img = line_detection(img)

    # #cv2.imshow('edge', edge_img)
    # #cv2.imshow('roi', roi_img)
    # cv2.imshow('xxx', processed_img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()
