import light_traffic_detection
import stop_sign_detection
#import finding_lanes
import measure_distance
import cv2
import numpy as np

vid = cv2.VideoCapture(0)

while (vid.isOpened()):
    _, frame = vid.read()

    # stop_coordinates = stop_sign_detection.stop(frame)
    # light_coordinates = light_traffic_detection.light(frame)

    # if len(stop_coordinates) == 0 and len(light_coordinates) == 0:
    #     print('tiếp tục di chuyển')
    # else:
    #     light_traffic_detection.decision_light(frame, light_coordinates)
    #     stop_sign_detection.decision_stop(stop_coordinates)
    #     measure_distance.distance(frame, stop_coordinates)
  
    cv2.imshow('xxx', frame)
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()



