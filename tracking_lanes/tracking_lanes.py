import cv2
import numpy as np
from matplotlib import pyplot as plt
import time


def analyzing_image(image):
    plt.imshow(image)
    plt.show()


def edge_detection(image):
    '''
        Edge detection: 
            _convert RGB image to grayscale image for more easily processing.
            _bluring image
            _edge detection by cv2.Canny function()
    '''

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # smoothing images = removing noise,
    blurred_image = cv2.blur(gray_image, (5, 5))
    edge_image = cv2.Canny(blurred_image, 50, 150)  # edge detection

    return edge_image


def region_of_interest(image):
    '''
        Extracting Region of Interest(RoI) from the edge image:
            _setting coordinates of a polygon that contains RoI
            _creating a black image (intensity = 0) with a white foreground which have the same coordinates with RoI
            _multiplying edge image by that black image
    '''
    edge_image = edge_detection(image)
    height = edge_image.shape[0]  # max value of y_axis
    width = edge_image.shape[1]  # max value of x_axis
    roi_coordinates = np.array([[(50, 400),
                                 (600, 400),
                                 (500, 100),
                                 (200, 100)]], np.int32)
    roi_area = np.zeros_like(edge_image)
    cv2.fillPoly(roi_area, roi_coordinates, 255)
    roi_image = cv2.bitwise_and(edge_image, roi_area)

    return roi_image


def lines_detection(image):
    '''
        A lane includes 2 lines.
        Using Hough Transform to detect lines, but there'll be a lot of lines in return.
    '''
    roi_image = region_of_interest(image)
    lines = cv2.HoughLinesP(roi_image, 1, np.pi/180, 100,
                            np.array([]), minLineLength=10, maxLineGap=10)
    #print('lines', lines)

    return lines


def lane_detection(image):
    '''
        A lane is 2 lines.
        So what we are looking for is averaged left line and right line.
        In order to do that, we need to calculate averaged slope and y_intercept,
        and then we use the line equation (y = x*slope + y_intercept) to find 2 points in each our averaged lines.
    '''
    
    try:
        lines = lines_detection(image)
        left_lines = []
        right_lines = []
        for line in lines:
            for x1, y1, x2, y2 in line:
                paramenters = np.polyfit((x1, x2), (y1, y2), 1)
                slope = paramenters[0]
                y_intercept = paramenters[1]
    
                if slope < 0:  # left line
                    left_lines.append((slope, y_intercept))
                else:  # right_line
                    right_lines.append((slope, y_intercept))
    
        if len(left_lines) != 0 and len(right_lines) != 0:
            averaged_left_line = np.average(left_lines, axis=0)
            averaged_right_line = np.average(right_lines, axis=0)
         
            lane = calculating_center_line(averaged_left_line, averaged_right_line)
            #print('lane:', lane)
            c = '0'
            return [lane], c

        elif len(right_lines) == 0 and len(left_lines) != 0:
            averaged_left_line = np.average(left_lines, axis=0)
            left_lane = calculating_new_x_y(averaged_left_line)
            #print('left lane:', left_lane)
            c = '2'
            return [left_lane], c

        elif len(left_lines) == 0 and len(right_lines) != 0:
            averaged_right_line = np.average(right_lines, axis=0)
            right_lane = calculating_new_x_y(averaged_right_line)
            #print('right lane:', right_lane)
            c = '1'
            return [right_lane], c


    except Exception as e:
        #print('error at tracking lane:', e)
        pass


def calculating_new_x_y(averaged_line):
    slope, y_intercept = averaged_line
    y1 = 400
    y2 = 200
    x1 = int((y1-y_intercept)/(slope))
    x2 = int((y2-y_intercept)/(slope))
    return [x1, y1, x2, y2]


def calculating_center_line(averaged_left_line, averaged_right_line):
    x1, y1, x2, y2 = calculating_new_x_y(averaged_right_line)
    x3, y3, x4, y4 = calculating_new_x_y(averaged_left_line)
    x1_cen = int((x1 + x3)/2)
    x2_cen = int((x2 + x4)/2)
    y1_cen = int((y1 + y3)/2)
    y2_cen = int((y2 + y4)/2)

    return [x1_cen, y1_cen, x2_cen, y2_cen]



def drawing_lane(original_image, copy_image):
    lane_image = np.zeros_like(original_image)
    try:
        lane, c = lane_detection(copy_image)
        #print('command:', c)
        if lane is not None:
            for line in lane:
                x1, y1, x2, y2 = line
                cv2.line(lane_image, (x1, y1), (x2, y2), (255, 255, 0), 10)

        lane_image = cv2.addWeighted(original_image, 0.8, lane_image, 1, 0)

        return lane_image, c
    except:
        cv2.putText(original_image, 'Out Lane', (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    4, (255, 255, 255), 1, cv2.LINE_AA)
        c = '3'
        return original_image, c
        pass


if __name__ == "__main__":
    last_time = time.time()

    image_path = r'C:\Users\DucTRung\Documents\data_set\tracking_lane\image_10_fps\lane0.jpg'
    image = cv2.imread(image_path)
    copy_image = np.copy(image)
    

    #edge_image = edge_detection(image)

    #roi_image = region_of_interest(image)

    #lines = lines_detection(image)
    #print('lines:', lines)

    #lane = lane_detection(copy_image)
    #print('lane:', lane)

    lane_image, c = drawing_lane(image, copy_image)
    print('command:', c)

    #analyzing_image(image)
    #cv2.imshow('original_img', image)
    #cv2.imshow('edge_img', edge_image)
    #cv2.imshow('roi_img', roi_image)
    #cv2.imshow('lines_img', lines_image)
    cv2.imshow('lane_img', lane_image)

    print('Thời gian đo được sau một lần xử lý của Khối xử lý: {} giây'.format(time.time() - last_time))

    cv2.waitKey(0)
    cv2.destroyAllWindows()
