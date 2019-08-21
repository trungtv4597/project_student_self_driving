import cv2
import numpy as np


def edge_detection(img):
    '''
        Edge detection: 
            _convert RGB image to grayscale image for more easily processing.
            _bluring image
            _edge detection by cv2.Canny function()
    '''
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edge_img = cv2.Canny(blur, 50, 150)  # edge detection
    return edge_img


def roi(img):
    '''
        Region of Interest(RoI):
            _Take RoI from edge iamge
    '''
    edge_img = edge_detection(img)
    height = edge_img.shape[0]  # max value of y_axis
    width = edge_img.shape[1]  # max value of x_axis
    poly = np.array([[
        (0+100, height-100),
        (width, height-100),
        (width, int(height/2)),
        (0+100, int(height/2))
    ]])  # coordinates of every to create RoI
    # an image includes all 0(black) pixel values
    black_img = np.zeros_like(edge_img)
    # convert all 0 pixel values into 255(white) in RoI
    cv2.fillPoly(black_img, poly, 255)
    # multiple binary previous black & white image with edge iamge to create RoI image (x*0 = 0, x*1 = x)
    roi_img = cv2.bitwise_and(edge_img, black_img)
    return roi_img


def averaged_left_right_lines(img, lines):
    '''
        Calculating averaged lines from a lot of lines found by .HoughLinesP() function:

    '''
    left_fit = []
    right_fit = []
    try:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            # Fit a polynomial ``p(x) = p[0] * x**deg + ... + p[deg]`` of degree `deg`to points `(x, y)`. Returns a vector of coefficients `p` that minimises the squared error.
            paramenters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = paramenters[0]
            y_intercept = paramenters[1]
            if slope < 0:  # left line
                left_fit.append((slope, y_intercept))
                left_fit_averaged = np.average(left_fit, axis=0)
            else:  # right_line
                right_fit.append((slope, y_intercept))
                right_fit_averaged = np.average(right_fit, axis=0)

        # if len(left_fit) == 0:
        #     slope, y_intercept = right_fit_averaged
        #     slope = 0 - slope
        #     y_intercept = 600 - y_intercept + 70
        #     left_fit.append((slope, y_intercept))
        #     left_fit_averaged = np.average(left_fit, axis=0)
        # if len(right_fit) == 0:
        #     slope, y_intercept = left_fit_averaged
        #     slope = 0 - slope
        #     y_intercept = 600 - y_intercept - 150
        #     right_fit.append((slope, y_intercept))
        #     right_fit_averaged = np.average(left_fit, axis=0)

        left_line = calcu_coordinates(img, left_fit_averaged)
        right_line = calcu_coordinates(img, right_fit_averaged)
        return np.array([left_line, right_line])
    except:
        #print('out lane')
        cv2.putText(img, 'Out Lane', (100, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2, cv2.LINE_AA)
        pass


def calcu_coordinates(img, line_parameters):
    '''
        Calculate coordicates of 2 points our averaged lines go through.
    '''
    slope, y_intercept = line_parameters
    y1 = img.shape[0]
    y2 = int(y1*(1-0.3))
    x1 = int((y1 - y_intercept)/slope)
    x2 = int((y2 - y_intercept)/slope)
    # print(x1,y1,x2,y2)
    return [[x1, y1, x2, y2]]


def lines_detection(img):
    '''
        Lanes is lines, so we can track a lane by detecting all lines in that
    '''
    roi_lane = roi(img)
    black_img = np.zeros_like(img)
    lines = cv2.HoughLinesP(roi_lane, 1, np.pi/180, 100,
                            np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = averaged_left_right_lines(img, lines)
    try:
        for line in averaged_lines:
            for x1, y1, x2, y2 in line:
                cv2.line(black_img, (x1, y1), (x2, y2), (255, 255, 0), 5)
                lines_img = cv2.addWeighted(img, 0.8, black_img, 1, 0)
        return lines_img
    except:
        pass