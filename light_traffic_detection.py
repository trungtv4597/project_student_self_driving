import cv2
import numpy as np


def light(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    light_cascade = cv2.CascadeClassifier('TrafficLight_HAAR_16Stages.xml')
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    light_coordinates = light_cascade.detectMultiScale(blur, 1.3, 5)

    for (x, y, w, h) in light_coordinates:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #cropped_img = image[y:y+h, x:x+w]
        #cv2.imshow('light', cropped_img)
        #cv2.imshow('image', image)

    return light_coordinates


def color(image, light_coordinates):
        # Morphological transformation, Dilation
    kernel = np.ones((5, 5), "uint8")
    # definig the range of red color
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    # defining the Range of yellow color
    yellow_lower = np.array([22, 60, 200], np.uint8)
    yellow_upper = np.array([60, 255, 255], np.uint8)

    # defining the Range of green color
    # green_lower = np.array([53, 210, 54], np.uint8)
    # green_upper = np.array([97, 255, 221], np.uint8)

    for (x, y, w, h) in light_coordinates:
        cropped_img = image[y:y+h, x:x+w]
        # converting bgr color space to hsv color space
        hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)

        # finding the range of red, green and yellow color in the image
        red = cv2.inRange(hsv, red_lower, red_upper)
        yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
        #green = cv2.inRange(hsv, green_lower, green_upper)

        # increment area of object
        red = cv2.dilate(red, kernel)
        #res = cv2.bitwise_and(cropped_img, cropped_img, mask=red)

        yellow = cv2.dilate(yellow, kernel)
        #res1 = cv2.bitwise_and(cropped_img, cropped_img, mask=yellow)

        #green = cv2.dilate(green, kernel)
        #res2 = cv2.bitwise_and(cropped_img, cropped_img, mask=green)

        # Tracking the Red Color
        (_, contours, hierarchy) = cv2.findContours(
            red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 30):
                # x, y, w, h = cv2.boundingRect(contour)
                # image = cv2.rectangle(cropped_img, (x, y),
                #                            (x+w, y+h), (0, 0, 255), 2)
                

                return 1

        # Tracking the yellow Color
        (_, contours, hierarchy) = cv2.findContours(
            yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 30):
                # x, y, w, h = cv2.boundingRect(contour)
                # image = cv2.rectangle(cropped_img, (x, y),
                #                            (x+w, y+h), (0, 255, 255), 2)
                
                return 2

def decision_light(image, light_coordinates):
    #if len(light_coordinates) == 0:

    if len(light_coordinates) != 0:
        print('đèn giao thông, chờ xác định loại đèn')
        if color(image, light_coordinates) == 1: 
            print('  đèn đỏ, dừng lại')
            cv2.putText(image, "red", (100, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
        elif color(image, light_coordinates) == 2: 
            print('  đèn vàng, dừng lại')
            cv2.putText(image, "yellow", (100, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255))
        else: 
            print('  đèn xanh, được phép di chuyển')
            cv2.putText(image, "green", (100, 100),
                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))


def video():
    cap = cv2.VideoCapture(0)
    while 1:
        ret, frame = cap.read()
        light_coordinates = light(frame)
        color_detect = color(frame, light_coordinates)
        decision_light(frame, light_coordinates)

        cv2. imshow('xxx', frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

# IMAGE:
        # red_light: C:\Users\DucTRung\Documents\OpenCV\light_traffic_detection\red_light.jpg

def image():
    img = cv2.imread(
        r'C:\Users\DucTRung\Documents\OpenCV\light_traffic_detection\red_light.jpg')
    light_coordinates = light(img)

    color_detect = color(img, light_coordinates)

    # if len(light_coordinates) == 0:
    #     print('không có đèn di chuyển bình thường')
    # else:
    #     print('có đèn giao thông, cần xác định màu')
    #     if color_detect == 1:
    #         print('đứng lại')
    #     else:
    #         print('có thể di chuyển')
    cv2.imshow('xxx', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
