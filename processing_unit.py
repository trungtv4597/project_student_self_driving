import urllib.request
import cv2
import numpy as np
import tracking_lanes
from tracking_lanes import lines_detection
import time
import urllib.request

root_url = "http://192.168.1.115/"


def sendRequest(url):
    n = urllib.request.urlopen(url)  # send request to ESP


def command(url, c):
    '''
        0: go_straight
        1: turn right
        2: turn left
        3: stop
    '''
    if c == 0:
        sendRequest(root_url+"/0")
    elif c == 1:
        sendRequest(root_url+"/1")
    elif c == 2:
        sendRequest(root_url+"/2")
    else:
        sendRequest(root_url+"/3")


if __name__ == '__main__':
    last_time = time.time()
    cap = cv2.VideoCapture(
        r'C:\Users\DucTRung\Documents\OpenCV\finding-lanes\Picture_test\video_test_udemy.mp4')
    while True:
        _, frame = cap.read()
        image = np.copy(frame)
        # Rotate image
        # (h, w) = frame.shape[:2]
        # center = (h//2, w//2)
        # M = cv2.getRotationMatrix2D(center, 270, 1)
        # image = cv2.warpAffine(frame, M, (h, w))

        # Process image
        #edge_image = edge_detection(image)
        #roi_image = region_of_interest(edge_image)
        processed_image, c = lines_detection(image)

        command(root_url, c)

        # Display image
        #cv2.imshow('original', frame)
        #cv2.imshow('edge', edge_image)
        #cv2.imshow('roi', roi_image)
        cv2.imshow('xxx', processed_image)

        #print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('x'):
            cv2.destroyAllWindows()
            cap.release()

    # image = cv2.imread(r"Picture_test\image_test.jpg")
    # img = np.copy(image)
    # # (h, w) = image.shape[:2]
    # # center = (w // 2, h // 2)
    # # M = cv2.getRotationMatrix2D(center, 270, 1)
    # # img = cv2.warpAffine(image, M, (h, w))

    # edge_img = edge_detection(img)
    # roi_img = region_of_interest(edge_img)
    # processed_img = image_processing(img)

    # #cv2.imshow('edge', edge_img)
    # #cv2.imshow('roi', roi_img)
    # cv2.imshow('xxx', processed_img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()
