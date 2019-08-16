import cv2
import numpy as np 




def edge_detection(copy_image):
    gray = cv2.cvtColor(copy_image, cv2.COLOR_RGB2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel,kernel), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def roi(edge):
    height = edge.shape[0]
    #width = edge.shape[1]
    poly = np.array([[(250,height),(1150,height), (670, 300)]])
    black_image = np.zeros_like(edge)
    cv2.fillPoly(black_image, poly, 255)
    roi = cv2.bitwise_and(edge, black_image)
    return roi


def slope(x1, y1, x2, y2):
    # source for calculating slope: https://cls.syr.edu/mathtuneup/grapha/Unit4/Unit4a.html
    slope = (y2 - y1) / (x2 -x1)
    return slope
def y_intercept(x1, y1, x2, y2):
    # phương trình đường thẳng: y = ax + b
    a = slope(x1, y1, x2, y2)
    b = y1 - a*x1
    return b


def make_coordinates(copy_image, line_parameters):
    slope, y_intercept = line_parameters
    y1 = copy_image.shape[0]
    y2 = 500
    x1 = int((y1 - y_intercept)/slope)
    x2 = int((y2 - y_intercept)/slope)
    #print(x1,y1,x2,y2)
    return [[x1,y1,x2,y2]]


def averaged_slope_intercept(copy_image, lines_image):
    left_fit = [] #chứa tọa độ đường thẳng trung bình bên trái
    right_fit = [] #chứa tọa độ đường thẳng trung bình bên phải 
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        #Fit a polynomial ``p(x) = p[0] * x**deg + ... + p[deg]`` of degree `deg`to points `(x, y)`. Returns a vector of coefficients `p` that minimises the squared error.
        paramenters = np.polyfit((x1,x2),(y1,y2), 1) # giải bài toán tìm slope và y-intercept của một đường thẳng đi qua 2 điểm
        slope = paramenters[0]
        y_intercept = paramenters[1]
        if slope < 0: #trong matplotlib, đường thẳng đi từ dưới lên về phía bên phải và ngược lại if slope > 0
            left_fit.append((slope, y_intercept))
            left_fit_averaged = np.average(left_fit, axis=0)
        else:
            right_fit.append((slope, y_intercept))
            right_fit_averaged = np.average(right_fit, axis=0)

    if len(left_fit) == 0:
        slope, y_intercept = right_fit_averaged
        slope = 0 - slope
        y_intercept = 600 - y_intercept + 70
        left_fit.append((slope, y_intercept))
        left_fit_averaged = np.average(left_fit, axis=0)
    if len(right_fit) == 0:
        slope, y_intercept = left_fit_averaged
        slope = 0 - slope
        y_intercept = 600 - y_intercept - 150
        right_fit.append((slope, y_intercept))
        right_fit_averaged = np.average(left_fit, axis=0)
    
    left_line = make_coordinates(copy_image, left_fit_averaged)
    right_line = make_coordinates(copy_image, right_fit_averaged)
    return np.array([left_line, right_line]) 



def line_detection(copy_image, lines):
    black_image = np.zeros_like(copy_image)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(black_image, (x1,y1), (x2,y2), (255,255,0), 5)
    return black_image  
     

#trackbar
# def nothing(x):
#     pass
# cv2.namedWindow('lines detection')
# cv2.createTrackbar('number of pixels', 'lines detection', 2, 50, nothing)
# cv2.createTrackbar('threshold of bin', 'lines detection', 50, 500, nothing)
# cv2.createTrackbar('minLineLength', 'lines detection', 40, 150, nothing)
# cv2.createTrackbar('maxLineGap', 'lines detection', 5, 20, nothing)
# n = cv2.getTrackbarPos('number of pixels', 'lines detection')
# t = cv2.getTrackbarPos('threshold of bin', 'lines detection')
# m1 = cv2.getTrackbarPos('minLineLength', 'lines detection')
# m2 = cv2.getTrackbarPos('maxlineGap', 'lines detection')

# image = cv2.imread(r'C:\Users\DucTRung\Documents\OpenCV\finding-lanes\test1.jpg')
# copy_image = np.copy(image)
# edge = edge_detection(copy_image)
# roi_lane = roi(edge)
# lines = cv2.HoughLinesP(roi_lane, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
# averaged_lines = averaged_slope_intercept(copy_image, lines)
# lines_image = line_detection(copy_image, averaged_lines)
# display_lines = cv2.addWeighted(copy_image, 0.8, lines_image, 1, 0)
# cv2.imshow('xxx',display_lines)
# #cv2.imwrite('toi_uu_anh.png', display_lines)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


video = cv2.VideoCapture(r'Picture_test\video_test_udemy.mp4')
while True:
    _,frame = video.read()
    copy_image = np.copy(frame)
    edge = edge_detection(copy_image)
    roi_lane = roi(edge)
    lines = cv2.HoughLinesP(roi_lane, 10, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = averaged_slope_intercept(copy_image, lines)
    lines_image = line_detection(copy_image, averaged_lines)
    display_lines = cv2.addWeighted(copy_image, 0.8, lines_image, 1, 0)
    cv2.imshow('xxx',display_lines)
    cv2.waitKey(1)
    
video.release()
cv2.destroyAllWindows()
