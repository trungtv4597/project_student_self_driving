import numpy as np
import cv2


def stop(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    stop_cascade = cv2.CascadeClassifier(r'C:\Users\DucTRung\Documents\GitHub\project_student_self_driving\image\Stopsign_HAAR_19Stages.xml')
    stop_coordinates = stop_cascade.detectMultiScale(blur, 1.3, 5)

    for (x, y, w, h) in stop_coordinates:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #cv2.imshow('stop sign', image)
        cv2.putText(image, "Stop", (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))

    return stop_coordinates


def decision_stop(stop_coordinates):
    # if len(stop_coordinates) == 0 :
    #    print('tiếp tục di chuyển')
    if len(stop_coordinates) != 0:
        print('biến báo STOP, dừng lại')


def video():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        _, frame = cap.read()
        #image = stop(frame)
        #decision_stop(image)
        cv2.imshow('img', frame)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    cap.release()
    cv2.destroyAllWindows()


def image():
    # C:\Users\DucTRung\Documents\OpenCV\traffic_signs_detection\stop_sign.JPG
    img = cv2.imread(
        r'C:\Users\DucTRung\Documents\OpenCV\traffic_signs_detection\stop_sign.JPG')
    stop_coordinates = stop(img)

    if len(stop_coordinates) == 0:
        print('di chuyển tiếp')
    else:
        print('biến stop, dừng lại')

    cv2.imshow('xxx', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
