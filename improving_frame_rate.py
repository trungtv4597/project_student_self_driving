import numpy as np 
import cv2
import imutils
from imutils.video import FPS
from imutils.video import WebcamVideoStream
from imutils.video import FileVideoStream
from tracking_lanes.tracking_lanes import drawing_lane



video_path = r'C:\Users\DucTRung\Documents\data_set\tracking_lane\ivcam_60_fps.avi'

# using read() from VideoCapture
cap = cv2.VideoCapture(1)
print("using VideoCapture")
fps = FPS().start()

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret is True:

        copy_image = np.copy(frame)
        lane_image, _ = drawing_lane(frame, copy_image)

        cv2.imshow('VideoCapture', lane_image)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

        fps.update()

    else:
        break

fps.stop()
print('Time:{:.2f}'.format(fps.elapsed()))
print('FPS:{:.2f}'.format(fps.fps()))
print('Number of frames:{:.2f}'.format(fps.fps()*fps.elapsed()))

cap.release()
cv2.destroyAllWindows()

# using WebcamVideoStream
wvs = WebcamVideoStream(src= 1).start()
print("\nusing WebcamVideoStream")
fps = FPS().start()

while True:
    frame = wvs.read()
    if frame is not None:

        copy_image = np.copy(frame)
        lane_image, _ = drawing_lane(frame, copy_image)

        cv2.imshow('WebcamVideoStream', lane_image)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

        fps.update()
    
    else:
        break

fps.stop()
print('Time:{:.2f}'.format(fps.elapsed()))
print('FPS:{:.2f}'.format(fps.fps()))
print('Number of frames:{:.2f}'.format(fps.fps()*fps.elapsed()))

wvs.stop()
cv2.destroyAllWindows()

# using FileVideoStream
fvs = FileVideoStream(1).start()
print('\nusing FileVideoStream')
fps = FPS().start()

while True:
    frame = fvs.read()
    if frame is not None:

        copy_image = np.copy(frame)
        lane_image, _ = drawing_lane(frame, copy_image)

        cv2.imshow('FileVideoStream', lane_image)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

        fps.update()
    
    else:
        break

fps.stop()
print('Time:{:.2f}'.format(fps.elapsed()))
print('FPS:{:.2f}'.format(fps.fps()))
print('Number of frames:{:.2f}'.format(fps.fps()*fps.elapsed()))

fvs.stop()
cv2.destroyAllWindows()  
        


