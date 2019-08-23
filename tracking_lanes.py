import cv2
import numpy as np
import time


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
        (width*(0.2), height),
        (width, height),
        (width, height*(0.7)),
        (width*(0.7), height*(0.5)),
        (width*(0.5), height*(0.5)),
        (width*(0.3), height*(0.7))]], np.int32)

    cv2.fillPoly(black_image, roi, 255)
    roi_image = cv2.bitwise_and(edge_image, black_image)
    return roi_image


def averaged_left_right_lines(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
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

        return averaged_lines, 0
    else:
        if len(right_fit) == 0:
            left_fit_average = np.average(left_fit, axis=0)
            left_line = make_points(image, left_fit_average)
            #print('right is none', left_line)
        
            return [left_line], 1
        elif len(left_fit) == 0:
            right_fit_average = np.average(right_fit, axis=0)
            right_line = make_points(image, right_fit_average)
            #print('left is none', right_line)
      
            return [right_line], 2
        else:
            pass           


def make_points(image, line):
    slope, intercept = line
    y1 = image.shape[0]
    y2 = int(y1*(0.5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return [[x1, y1, x2, y2]]


def lines_detection(image):
    #black_image = np.zeros_like(image)
    edge_image = edge_detection(image)
    roi_image = region_of_interest(edge_image)
    lines = cv2.HoughLinesP(roi_image, 1, np.pi/180, 100,
                            minLineLength=10, maxLineGap=50)
    averaged_lines, c = averaged_left_right_lines(image, lines)

    try:
        for line in averaged_lines:
            for x1, y1, x2, y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), (255, 255, 0), 20)
        return image, c
    except:
        cv2.putText(image, "OUT LANE", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (255, 0, 0), lineType=cv2.LINE_AA)
        return image, 3

