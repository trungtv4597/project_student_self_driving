import cv2
from tracking_lanes.tracking_lanes import drawing_lane, region_of_interest
import numpy as np
import time
from ws4py.client.threadedclient import WebSocketClient
from imutils.video import WebcamVideoStream
import time


class DummClient(WebSocketClient):
    def opened(self):  # handshake is done
        print('Websocket mở!')

    def closed(self, code, reason=None):
        print('Kết nối đóng!', code, reason)

    def received_message(self, m):
        print('Thông điệp từ server:', m)


if __name__ == "__main__":

    esp8266host = 'ws://192.168.10.107:81/'
    ws = DummClient(esp8266host)
    ws.connect()  # Websocket handshake protocol

    video_path = r'C:\Users\DucTRung\Documents\data_set\tracking_lane\ivcam_15_fps.avi'

    stream = WebcamVideoStream(src= 0).start()
    try:
        while True:
            
            frame = stream.read()
            
            if frame is not None:
                #frame = cv2.flip(frame, 0)
                
                copy_image = np.copy(frame)

                roi_image = region_of_interest(copy_image)

                lane_image, c = drawing_lane(frame, copy_image)

                print('command: ', c)
        
                ws.send(c)

                cv2.imshow('roi', roi_image)
                cv2.imshow('lane', lane_image)

                if cv2.waitKey(60) & 0xFF == ord('x'):
                    ws.send('3')
                    ws.close()
                    break
            else:
                break

        stream.stop()
        cv2.destroyAllWindows()
    except Exception as error:
        print('error:', error)
        ws.send('3')
        ws.close()
