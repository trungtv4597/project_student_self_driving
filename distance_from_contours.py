import cv2
import numpy as np


def image_processing(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(hsv, (5, 5), 0)
    return blur


def finding_contours(image):
    # Contours is a curve joining all the continuous points having same color or intensity.
    # we choose red color.
    kernel = np.ones((5, 5), "uint8")
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    hsv = image_processing(image)
    red_thresh = cv2.inRange(hsv, red_lower, red_upper)
    red_dilate = cv2.dilate(red_thresh, kernel)

    # gray = image_processing(image)
    # _, thresh = cv2.threshold(gray, 127, 255, 0)

    img2, contours, hierarchy = cv2.findContours(
        red_dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.imshow('contours image', img2)

    return contours


def biggest_contour(image):
    contours = finding_contours(image)
    x = []
    if contours != 0:
        for number, contour in enumerate(contours):
            contour_size = cv2.contourArea(contour)
            x = np.append(x, int(contour_size))
            #print('size:', contour_size,'\nx:', x)

            if contour_size == np.max(x, axis=0) and contour_size > 1000:
                cnt = contours[number]
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

                f = 567.5
                W = 11.6
                d = int((f * W)/w)
                print('distance: ', d)
                cv2.putText(image, 'distance: ' + str(d) + " cm", (100, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))
    return image


def capturing_frame():
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        _, frame = cap.read()

        contours_img = biggest_contour(frame)

        #cv2.imshow('xxx', frame)
        cv2.imshow('contours', contours_img)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    cap.release()
    cv2.destroyAllWindows()

#capturing_frame()


def x():
    x = [1, 2, 3, 1, 2, 9, 4, 5]
    for n, i in enumerate(x):
        y = i + 1
        if y is max(x):
            print(y)
            print(n)



