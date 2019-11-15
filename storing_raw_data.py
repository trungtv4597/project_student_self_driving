import cv2
import numpy as np


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)


    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    out_15_frame = cv2.VideoWriter(r'C:\Users\DucTRung\Documents\data_set\tracking_lane\ivcam_15_fps.avi', cv2.VideoWriter_fourcc(
        'M', 'J', 'P', 'G'), 15, (frame_width, frame_height))

    out_25_frame = cv2.VideoWriter(r'C:\Users\DucTRung\Documents\data_set\tracking_lane\ivcam_25_fps.avi', cv2.VideoWriter_fourcc(
        'M', 'J', 'P', 'G'), 25, (frame_width, frame_height))

    out_30_frame = cv2.VideoWriter(r'C:\Users\DucTRung\Documents\data_set\tracking_lane\ivcam_30_fps.avi', cv2.VideoWriter_fourcc(
        'M', 'J', 'P', 'G'), 30, (frame_width, frame_height))
    
    out_60_frame = cv2.VideoWriter(r'C:\Users\DucTRung\Documents\data_set\tracking_lane\ivcam_60_fps.avi', cv2.VideoWriter_fourcc(
        'M', 'J', 'P', 'G'), 60, (frame_width, frame_height))

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Unable to read camera feed")
    while(True):
        ret, frame = cap.read()

        if ret == True:
            image = cv2.flip(frame, 0)

            # Write the frame into the file 'output.avi'
            out_15_frame.write(image)
            out_25_frame.write(image)
            out_30_frame.write(image)
            out_60_frame.write(image)

            # Display the resulting frame
            cv2.imshow('frame', image)

            # Press Q on keyboard to stop recording
            if cv2.waitKey(67) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture and video write objects
    cap.release()
    out_15_frame.release()
    out_25_frame.release()
    out_30_frame.release()
    out_60_frame.release()

    # Closes all the frames
    cv2.destroyAllWindows()
