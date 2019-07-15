import cv2
import numpy as np
import keras
from keras.models import load_model


def img_preprocess(img):
    img = copy_frame[350:,:,:]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img,  (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img/255
    return img


if __name__ == "__main__":
    model = load_model('model_generator.h5')
    cap = cv2.VideoCapture(
        r"C:\Users\DucTRung\Documents\OpenCV\finding-lanes\Picture_test\video_test.mp4")
    while(cap.isOpened()):
        _, frame = cap.read()
        copy_frame = np.copy(frame)
        processed_image = img_preprocess(copy_frame)
        image = np.array([processed_image])
        steering_radians = float(model.predict(image))
        if steering_radians < 0:
            steering_degrees = np.absolute(np.degrees(steering_radians))
            print('turn left_steering angle:', steering_degrees)
        elif steering_radians > 0:
            steering_degrees = np.absolute(np.degrees(steering_radians))
            print('turn right_steering angle:', steering_degrees)
        else:
            steering_degrees = np.absolute(np.degrees(steering_radians))
            print('go straight_steering angle:', steering_degrees)
        cv2.putText(frame, str(steering_degrees), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow('xxx', frame)
        if cv2.waitKey(1) == ord('x'):
            break  
    cap.release()
    cv2.destroyAllWindows()
