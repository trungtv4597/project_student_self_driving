import urllib.request
import cv2
import numpy as np
import tracking_lanes
from tracking_lanes import lines_detection

#url = '/shot.jpg'
if __name__ == "__main__":
    cap = cv2.VideoCapture(r'C:\Users\DucTRung\Documents\OpenCV\finding-lanes\Picture_test\cc_video.mp4')
    while True:
        # frameResp = urllib.request.urlopen(url)
        # frameNp = np.array(bytearray(frameResp.read()), dtype= np.uint8)
        # frame = cv2.imdecode(frameNp, -1)

        _, frame = cap.read()
        if frame is not None:
            # Rotation:
            # (h, w) = frame.shape[:2]
            # center = (w / 2, h / 2)
            # M = cv2.getRotationMatrix2D(center, 270, 1)
            # img = cv2.warpAffine(frame, M, (h, w))

            copy_img = np.copy(frame)
            img = lines_detection(copy_img) 
            cv2.imshow('xxx', img)
            if cv2.waitKey(1) & 0xFF == ord('x'):
                break
        else:
            break
    cv2.destroyAllWindows()
    cap.release()
