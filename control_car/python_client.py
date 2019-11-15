import time
from ws4py.client.threadedclient import WebSocketClient
import cv2
import numpy as np
import keras
from keras.models import load_model
import random


class DummClient(WebSocketClient):
    def opened(self):
        print('Websocket open')

    def closed(self, code, reason=None):
        print('Connection closed down', code, reason)

    def received_message(self, m):
        print('cc: ', m)


def processing_image(image):
    image = image[100:400, 0:500]
    #image = image[120:450, 120:837]  # region of interest
    image = cv2.resize(image, (32, 32))  # (width, height)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.bitwise_not(image)
    image = cv2.equalizeHist(image)
    image = image/255
    input_image = image.reshape(1, 32, 32, 1)
    return input_image


if __name__ == "__main__":
    model = load_model('driveless_leNet_model.h5')

    esp8266host = 'ws://192.168.43.85:81/'
    ws = DummClient(esp8266host)
    ws.connect()

    cap = cv2.VideoCapture(0)
    try:
        last_time = time.time()
        
        while (cap.isOpened()):
            _, frame = cap.read()

            processed_image = processing_image(frame)

            driving_decision = model.predict_classes(processed_image)
            print('dự đoán:', driving_decision[0])

            ws.send(str(driving_decision[0]))

            print('loop took {} seconds'.format(time.time() - last_time))
            last_time = time.time()

            cv2.imshow('input image', frame)
            if cv2.waitKey(50) == ord('x'):
                ws.send('3')
                ws.close()
                break
        cap.release()
        cv2.destroyAllWindows()

    except:
        ws.send('3')
        ws.close()
        print('')