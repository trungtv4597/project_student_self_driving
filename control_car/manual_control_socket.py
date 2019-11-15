from msvcrt import getwch, kbhit
import time
from ws4py.client.threadedclient import WebSocketClient
import cv2
import numpy as np


class DummClient(WebSocketClient):
    def opened(self):
        print('Websocket open')

    def closed(self, code, reason=None):
        print('Connection closed down', code, reason)

    def received_message(self, m):
        print('cc: ', m)


if __name__ == "__main__":

    esp8266host = 'ws://192.168.1.2:81/'
    ws = DummClient(esp8266host)
    ws.connect()

    # option = ['x', 'w', 'q', 'e', 's', 'a', 'd']
    try:
        last_time = time.time()

        while True:

            while not kbhit():
                time.sleep(0.5)
                ws.send(str(3))

            while kbhit():
                time.sleep(0.1)
                command = getwch()
                print(command)
                ws.send(command)

                # if command == 'w':
                #     ws.send(str(0))
                # elif command == 'q':
                #     ws.send(str(1))
                # elif command == 'e':
                #     ws.send(str(2))
                # else:
                #     ws.send(str(3))

                print('loop took {} seconds'.format(time.time() - last_time))
                last_time = time.time()

    except KeyboardInterrupt:
        ws.send(str(3))
        ws.close()

     
