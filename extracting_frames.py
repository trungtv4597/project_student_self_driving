import numpy as np
import cv2
from tracking_lanes.tracking_lanes import drawing_lane

count = 0

video_paths = [r'C:\Users\DucTRung\Documents\data_set\tracking_lane\tracking_lane_curve.avi', '']
for i in video_paths:
    print('video path:', i)
    cap = cv2.VideoCapture(i)

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:

            cv2.imwrite(r'C:\Users\DucTRung\Documents\data_set\tracking_lane\image_test\xxx%d.jpg' %count, frame)

            cv2.waitKey(1)

            print('frame: ', count)

            count += 1

            # if count == 3:
            #     break

        else:
            break

    cap.release()
    cv2.destroyAllWindows()
