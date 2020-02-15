# Bài Viết Tóm Tắt Đề Tài

* Demo video
[Demo_video](https://www.youtube.com/watch?v=ZmLJjx38W1Q)

## Mục tiêu đề tài
Nâng cấp một chiếc xe điều khiển từ xa trở thành xe tự hành bằng áp dụng kỹ thuật xử lý ảnh và cảm biến: 
* Xác định và đi đúng làn đường quy định
* Tự động tránh vật cản.

## Tổng quan về giải thuật áp dụng trong đề tài

Xác định làn đường:
* Áp dụng kỹ thuật Hough Transform trong xử lý ảnh để xác định làn đường. 

![](https://github.com/trungtv4597/project_student_self_driving/blob/master/images/hough_transform_work_flow.png)

Tự động tránh vật cản:
* Sử dụng cảm biến siêu âm, HC-SR04, để đo khoảng cách tới vật cản.

![](https://github.com/trungtv4597/project_student_self_driving/blob/master/images/hc-sr04.png)

Thiết kế hệ thống

![](https://github.com/trungtv4597/project_student_self_driving/blob/master/images/system_design.jpg)

## Kết quả thức hiện đề tài

* Dựa trên việc có thể xác định được làn đường, xe có thể phán đoán hướng di chuyển và thậm chí còn có thể cảnh báo không đi đúng làn đường

![](https://github.com/trungtv4597/project_student_self_driving/blob/master/images/results2.png)
