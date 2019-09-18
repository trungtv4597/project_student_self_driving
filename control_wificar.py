import cv2
import numpy as np
from urllib import request
import keras
from keras.models import load_model


def send_request(url):
    request.urlopen(url)


def command_to_esp(esp_url, d):
    if d == 0:
        print('go straight')
        return send_request(esp_url+"/0")
    elif d == 1:
        print('turn left')
        return send_request(esp_url+"/1")
    elif d == 2:
        print('turn right')
        return send_request(esp_url+"/2")


def processing_image(image):
    width = image.shape[1]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    crop = blur[100:400, 0:width]
    equalize = cv2.equalizeHist(crop)
    normalize = equalize/255
    resized_image = cv2.resize(normalize, (28, 28))
    array_image = np.asarray(resized_image)
    input_image = array_image.reshape(1, 28, 28, 1)
    return input_image


esp_url = 'http://192.168.1.6/'
model = load_model('self_driving\driveless_model.h5')
cap = cv2.VideoCapture(0)
while (cap.isOpened()):
    _, frame = cap.read()
    image = cv2.flip(frame, 1)
    processed_image = processing_image(image)

    driving_decision = model.predict_classes(processed_image)

    command_to_esp(esp_url, driving_decision[0])

    cv2.imshow('xxx', frame)
    if cv2.waitKey(47) == ord('x'):
        send_request(esp_url+'/stop')
        break
cap.release()
cv2.destroyAllWindows()
