import urllib.request
import cv2
import numpy as np
import tracking_lanes
from tracking_lanes import lines_detection

#url = '/shot.jpg'
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        # frameResp = urllib.request.urlopen(url)
        # frameNp = np.array(bytearray(frameResp.read()), dtype= np.uint8)
        # frame = cv2.imdecode(frameNp, -1)

        _, frame = cap.read()
        if frame is not None:
            # Rotation:
            (h, w) = frame.shape[:2]
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, 270, 1)
            img = cv2.warpAffine(frame, M, (h, w))

            #img = cv2.flip(frame, 1)
            copy_img = np.copy(img)
            cc = lines_detection(copy_img) 
            cv2.imshow('xxx', cc)
            if cv2.waitKey(1) & 0xFF == ord('x'):
                break
        else:
            break
    cv2.destroyAllWindows()
    cap.release()
