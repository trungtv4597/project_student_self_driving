from tracking_lanes.tracking_lanes import lane_detection, drawing_lane, edge_detection, region_of_interest
import cv2
import numpy as np
import time

        

if __name__ == "__main__":
    video_path = r'C:\Users\DucTRung\Documents\data_set\tracking_lane\tracking_lane_curve.avi'
    cap = cv2.VideoCapture(video_path)
    image_directory = r'C:\Users\DucTRung\Documents\data_set\tracking_lane\image_test'
    count = 0
    last_time = time.time()
    try:

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret is True:
                copy_image = np.copy(frame)

                #edge_image = edge_detection(copy_image)
                #roi_image = region_of_interest(copy_image)
                lane_image, _ = drawing_lane(frame, copy_image)

                cv2.imwrite(image_directory+'\lane%d.jpg' %count, lane_image)
                count += 1
                cv2.imshow('xxx', lane_image)

                print('loop: {} second'.format(time.time() - last_time)) 
                last_time = time.time()

                if cv2.waitKey(1) & 0xFF == ord('x'):
                    break
            else:
                break
    except Exception as error:
        print(error)
        print('time measuring:', time.time() - last_time)
    cap.release()
    cv2.destroyAllWindows()