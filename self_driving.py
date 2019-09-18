import cv2
import numpy as np
import keras
from keras.models import load_model


def processing_image(image):
    width = image.shape[1]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    crop = blur[100:400, 0:width]
    equalize = cv2.equalizeHist(crop)
    normalize = equalize/255
    resized_image = cv2.resize(normalize, (28, 28))
    array_image = np.asarray(resized_image)
    input_image = array_image.reshape(1, 28, 28, 1)
    return input_image


def driving_prediction(image):
    processed_image = processing_image(image)
    #print('shape of processed iamge:', processed_image.shape)
    prediction = model.predict_classes(processed_image)
    #print('prediction', prediction[0])
    # if prediction[0] == 0:
    #     print('go straight')
    # elif prediction[0] == 1:
    #     print('turn left')
    # if prediction[0] == 2:
    #     print('turn right')
    return prediction[0]


if __name__ == "__main__":
    model = load_model('self_driving\driveless_model.h5')
    cap = cv2.VideoCapture(
        r"C:\Users\DucTRung\Documents\Machine_Learning\Deep_Learning\Keras\work_space\self_driving\data_raw\curl_left_lane.avi")
    while(cap.isOpened()):
        _, frame = cap.read()
        copy_frame = np.copy(frame)

        driving_prediction(copy_frame)

        cv2.imshow('xxx', frame)
        if cv2.waitKey(10) == ord('x'):
            break
    cap.release()
    cv2.destroyAllWindows()
