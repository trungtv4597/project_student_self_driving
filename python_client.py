import stop_sign_detection
import urllib.request
import cv2

root_url = "http://192.168.1.8/"


def sendRequest(url):
    n = urllib.request.urlopen(url)  # send request to ESP

def decision_stop(stop_coordinates):
    # if len(stop_coordinates) == 0 :
    #    print('tiếp tục di chuyển')
    if len(stop_coordinates) != 0:
        print('biến báo STOP, dừng lại')
        sendRequest(root_url+"/red")
    else:
        print('pass')
        sendRequest(root_url+"/pass")

cap = cv2.VideoCapture(0)
while cap.isOpened():
    _, frame = cap.read()
    stop_coor = stop_sign_detection.stop(frame)
    decision_stop(stop_coor)
    
    cv2.imshow('img', frame)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break
cap.release()
cv2.destroyAllWindows()
