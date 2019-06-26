# Tìm tiêu cự của camera (webcam laptop lenovo G640)
# 	F = (P * D) / W
# 	với vật thể làm mẫu là biển báo Stop được hiển thị trên điệ thoại có:
# 			W =  5.5 (cm)
# 			P =  150 (pixel)
# 			xét D = 20

def calculate_focal_length():
    w = input('độ rộng của vật thể theo cm: ')
    w = float(w)
    p = input('độ rộng của vật thể theo pixel: ')
    p = float(p)
    d = input('khoảng cách thiết lập từ camera tới vật thể theo cm: ')
    d = float(d)
    f = ((p * d) / w)
    #print('focal length: ',f, ' cm')
    return [f, w]




# x = calculate_focal_length()
# f = x[0]
# w = x[1]
# print(f)
# print(w)



