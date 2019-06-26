import cv2
import numpy as np
import matplotlib.pyplot as plt
import math


def canny(copy_image):
    # convert image to grayscale
    gray = cv2.cvtColor(copy_image, cv2.COLOR_RGB2GRAY)
    # reduce Noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # edges detection
    canny = cv2.Canny(blur, 50, 150)
    return canny


def roi(edge_img):
    # xác định một hình đa giác với các tọa độ x , y mong muốn
    height = edge_img.shape[0]
    width = edge_img.shape[1]
    polygons = np.array(
        [[(200, height), (1100, height), (800, 500), (400, 500)]], np.int32)
    # modify every pixels to be 0 (black) but inside polygon
    mask = np.zeros_like(edge_img)
    cv2.fillPoly(mask, polygons, 255)
    # canny * mask
    masked_image = cv2.bitwise_and(edge_img, mask)
    cv2.line(edge_img, (200, height), (350, 500), (255, 255, 0), 5)
    cv2.line(edge_img, (1100, height), (900, 500), (255, 255, 0), 5)
    return masked_image


def display_lines(img, lines):
    line_image = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            # reshape it into a one dimensional array with four elements
            x1, y1,  x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


def average_slope_intercept(image, lines):
    left_fit = []  # list
    right_fit = []
    if lines is None:
        return None
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        # line function: y = slope*x +y_intercept
        # quy định x1,x2 là SLOPE, y1,y2 là INTERCEPT
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            # append = thêm phần tử vào list.
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
        if len(left_fit) == 0:
            left_fit.append(((-1), 1000))
        if len(right_fit) == 0:
            right_fit.append((1, 1))
    # axis = 0: y_axis trục tung
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = lines_coordinates(image, left_fit_average)
    right_line = lines_coordinates(image, right_fit_average)
    #print('left line', left_line)
    #print('righ line', right_line)
    return np.array([left_line, right_line])


def lines_coordinates(image, line_paraments):
    slope, intercept = line_paraments
    y1 = image.shape[0]  # .shape[0]: height of image
    # it mean it will start from y1 (bottom of image = 704) to y2(704*3/5 = 422)
    y2 = 500
    # y = slope*x +y_intercept ==> x = (y- y_intercept)/slope
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])


def centerline_coordinates(lines):
    left = lines[0, :]
    lx1 = left[0]
    ly1 = left[1]
    lx2 = left[2]
    ly2 = left[3]
    right = lines[1, :]
    rx1 = right[0]
    ry1 = right[1]
    rx2 = right[2]
    ry2 = right[3]

    cx1 = int((1/2) * (lx1 + rx1))
    cy1 = int((1/2) * (ly1 + ry1))
    cx2 = int((1/2) * (lx2 + rx2))
    cy2 = int((1/2) * (ly2 + ry2))

    return np.array([cx1, cy1, cx2, cy2])


def centerline(image, lines):
    black = np.zeros_like(image)
    cx1, cy1, cx2, cy2 = centerline_coordinates(lines)
    left = lines[0, :]
    lx1 = left[0]
    ly1 = left[1]
    right = lines[1, :]
    rx1 = right[0]
    ry1 = right[1]
    cv2.line(black, (cx1, cy1), (cx2, cy2), (255, 255, 255), 5)
    cv2.line(black, (lx1, ly1), (cx1, cy1), (0, 255, 0), 5)
    cv2.line(black, (rx1, ry1), (cx1, cy1), (0, 0, 255), 5)
    #cv2.circle(black, (cx2, cy2), 5, (255, 255, 0), 5)
    return black


def calculate_angle(lines):  # equation: a*b = len(a)*len(b)*cos(pi)

    # coordinates of points
    cx1, cy1, cx2, cy2 = centerline_coordinates(lines)
    root = [cx1, cy1]  # root point
    c = [cx2, cy2]  # end point of vector center

    left = lines[0, :]
    lx = left[0]
    ly = left[1]
    l = [lx, ly]  # end point of vector left

    right = lines[1, :]
    rx = right[0]
    ry = right[1]
    r = [rx, ry]  # end point of vector right
    #print('c1:',root, '\nc2:', c, '\nl1:', l, '\nr1:', r)

    # coordinates of vectors
    vector_c = np.array(c) - np.array(root)  # vector_center
    vector_l = np.array(l) - np.array(root)  # vector_buttom_left
    vector_r = np.array(r) - np.array(root)  # vector_buttom_right
    #print('vector c:', vector_c, '\nvector l:', vector_l, '\nvector r:', vector_r )

    # length of vectors
    len_vc = np.sqrt(np.square(vector_c[0]) + np.square(vector_c[1]))
    len_vl = np.sqrt(np.square(vector_l[0]) + np.square(vector_l[1]))
    len_vr = np.sqrt(np.square(vector_r[0]) + np.square(vector_r[1]))
    #print('length of vector center:', len_vc, '\nlength of vector left:', len_vl, '\nlength of vector right:', len_vr)

    # multiplying 2 vector
    c_l = np.dot(vector_c, vector_l)
    c_r = np.dot(vector_c, vector_r)

    # calculate angel
    radian_left = np.arccos(c_l/(len_vc*len_vl))
    radian_right = np.arccos(c_r/(len_vc*len_vr))
    degrees_left = np.absolute(np.degrees(radian_left))
    degrees_right = np.absolute(np.degrees(radian_right))
    #print ('degree of left:', degree_left, '\ndegree of right:', degree_right)

    degrees = np.array([degrees_left, degrees_right])
    return degrees


def turning_by_degrees(image, angle):
    degrees_left, degrees_right = angle
    #print('left: ', degrees_left, '\nright: ', degrees_right)
    if degrees_left < degrees_right:
        degrees = int(degrees_left)
        print('turn left: ', 90-degrees, '*')
        cv2.putText(image, str(90-degrees)+'* turn left', (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
    elif degrees_right < degrees_left:
        degrees = int(degrees_right)
        print('turn right: ', 90-degrees, '*')
        cv2.putText(image, str(90-degrees)+'* turn right', (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
    else:
        degrees = int(degrees_left)
        print('go straight: ', 90-degrees, '*')
        cv2.putText(image, str(90-degrees)+'* go straight', (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
    return image


# image:    
# img = cv2.imread(
#     r'C:\Users\DucTRung\Documents\OpenCV\finding-lanes\Picture_test\image_test.jpg')
# copy_img = np.copy(img)
# edge_img = canny(copy_img)
# roi_img = roi(edge_img)
# lines = cv2.HoughLinesP(roi_img, 2, np.pi/180, 100,
#                         np.array([]), minLineLength=40, maxLineGap=5)
# averaged_lines = average_slope_intercept(copy_img, lines)
# lines_image = display_lines(copy_img, averaged_lines)
# lines_display = cv2.addWeighted(lines_image, 1, img, 0.8, 1)
# centerline_img = centerline(copy_img, averaged_lines)
# centerline_display = cv2.addWeighted(centerline_img, 1, lines_display, 0.7, 1)
# angle = calculate_angle(averaged_lines)
# turning = turning_by_degrees(centerline_display, angle)
# cv2.imshow('xxx', centerline_display)
# #cv2.imwrite('centerline.jpg', centerline_img)
# cv2.waitKey(0)

# video:
# cap = cv2.VideoCapture(
#     r"C:\Users\DucTRung\Documents\OpenCV\finding-lanes\Picture_test\video_test_udemy.mp4")
# while(cap.isOpened()):
#     _, frame = cap.read()
#     copy_img = np.copy(frame)
#     edge_img = canny(copy_img)
#     roi_img = roi(edge_img)
#     lines = cv2.HoughLinesP(roi_img, 2, np.pi/180, 100,
#                             np.array([]), minLineLength=40, maxLineGap=5)
#     averaged_lines = average_slope_intercept(copy_img, lines)

#     lines_image = display_lines(copy_img, averaged_lines)
#     lines_display = cv2.addWeighted(lines_image, 1, frame, 0.8, 1)

#     centerline_img = centerline(copy_img, averaged_lines)
#     centerline_display = cv2.addWeighted(
#         centerline_img, 1, lines_display, 0.7, 1)
#     angle = calculate_angle(averaged_lines)
#     turning = turning_by_degrees(centerline_display, angle)

#     cv2.imshow("xxx", turning)
#     if cv2.waitKey(1) == ord('x'):
#         break
# cap.release()
# cv2.destroyAllWindows()
