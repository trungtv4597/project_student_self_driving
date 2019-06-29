import numpy as np
import cv2

# camera Lab: d = 40cm & w = 5.5 -> p = 211  
# camera Lab: d = 20cm & w = 5.5 -> p = 411
# camera Lab: d = 600cm & w = 5.5 -> p = 142


def stop(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    stop_cascade = cv2.CascadeClassifier('Stopsign_HAAR_19Stages.xml')
    stop_coordinates = stop_cascade.detectMultiScale(blur, 1.3, 5)

    for (x, y, w, h) in stop_coordinates:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # cv2.imshow('stop sign', image)
        cv2.putText(image, 'Traffic Signal: ' + "Stop", (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))

        f = local_length()[0]
        W = local_length()[1]
        d = int((f * W)/w)
        cv2.putText(image, 'distance: ' + str(d) + " cm", (100, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))

    return stop_coordinates


def local_length():
        # first, we need to know local_length of our camera which is uesed by this formula: f = ((p * d) / w)
        # in this situation, i'm using webcam from laptop lenovo G460:
    p = 156     # width of the image in pixels
    d = 20      # set-up distance for measuring focal length     
    w = 5.5     # width of the object in cm
    f = ((p * d) / w)
    return [f, w]


def video():
    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()
        stop(frame)

        cv2.imshow('img', frame)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    cap.release()
    cv2.destroyAllWindows()


video()
