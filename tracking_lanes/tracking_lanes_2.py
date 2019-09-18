import cv2
import numpy as np


def rotate_image(image):
    (h, w) = image.shape[:2]
    center = (h//2, w//2)
    degree = 270
    M = cv2.getRotationMatrix2D(center, degree, 1)
    image = cv2.warpAffine(image, M, (h, w))
    return image


def edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)
    edge_image = cv2.Canny(blur, 50, 150)
    return edge_image


def region_of_interest(edge_image):
    #edge_image = edge_detection(image)
    height = edge_image.shape[0]
    width = edge_image.shape[1]
    black_image = np.zeros_like(edge_image)

    roi = np.array([[
        (0, height),
        (width, height),
        (width, 0),
        #(250, 350),
        #(50, 350),
        (0, 0)]], np.int32)

    cv2.fillPoly(black_image, roi, 255)
    roi_image = cv2.bitwise_and(edge_image, black_image)
    return roi_image


def averaged_left_right_lines(image, lines):
    try:
        left_fit = []
        right_fit = []
        for line in lines:
            for x1, y1, x2, y2 in line:
                # Numpy polyfit function
                # fit = np.polyfit((x1, x2), (y1, y2), 1)
                # slope = fit[0]
                # intercept = fit[1]

                # Numpy linalg lstsq function
                x = np.array([x1, x2])
                y = np.array([y1, y2])
                A = np.vstack([x, np.ones(len(x))]).T
                slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]

                if slope < 0:  # y is reversed in image
                    left_fit.append((slope, intercept))
                else:
                    right_fit.append((slope, intercept))

        if len(right_fit) != 0 and len(left_fit) != 0:
            left_fit_average = np.average(left_fit, axis=0)
            right_fit_average = np.average(right_fit, axis=0)
            left_line = make_points(image, left_fit_average)
            right_line = make_points(image, right_fit_average)
            averaged_lines = [left_line, right_line]
            return averaged_lines, 1
        else:
            if len(right_fit) == 0:
                left_fit_average = np.average(left_fit, axis=0)
                left_line = make_points(image, left_fit_average)
                #print('right is none', left_line)
                return [left_line], 2
            elif len(left_fit) == 0:
                right_fit_average = np.average(right_fit, axis=0)
                right_line = make_points(image, right_fit_average)
                #print('left is none', right_line)
                return [right_line], 3
    except:
        return None, 0


def make_points(image, line):
    slope, intercept = line
    y1 = image.shape[0]
    y2 = 400
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return [[x1, y1, x2, y2]]


def line_detection(image):
    #black_image = np.zeros_like(image)
    copy_image = np.copy(image)
    edge_image = edge_detection(copy_image)
    roi_image = region_of_interest(edge_image)
    lines = cv2.HoughLinesP(roi_image, 1, np.pi/180, 100,
                            minLineLength=4, maxLineGap=50)
    averaged_lines, c = averaged_left_right_lines(image, lines)
    #print('averaged lines: ', averaged_lines, 'c: ', c)
    try:
        for line in averaged_lines:
            for x1, y1, x2, y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), (255, 255, 0), 20)
        return image, c
    except:
        cv2.putText(image, "OUT LANE", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (255, 0, 0), lineType=cv2.LINE_AA)
        return image, c
