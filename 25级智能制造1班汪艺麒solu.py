import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (12, 8)

def show_img(imgs: np.ndarray) -> None:
    plt.figure()
    for idx, img in enumerate(imgs):
        plt.subplot(1, len(imgs), idx + 1)
        if len(img.shape) == 2:
            plt.imshow(img, cmap='gray')
        elif len(img.shape) == 3:
            plt.imshow(img[:, :, ::-1]) 
    plt.show()
#定义各颜色的HSV阈值
lower_purple = np.array([10, 30, 30])
upper_purple = np.array([25, 255, 255])
lower_red1 = np.array([0, 43, 46])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([175, 43, 46])
upper_red2 = np.array([180, 255, 255])
lower_blue = np.array([150, 43, 46])
upper_blue = np.array([165, 255, 255])
cam = cv2.VideoCapture("res/output1.avi")
cnt = 0
while True:
    ret, frame = cam.read()
    frame = cv2.rotate(frame,cv2.ROTATE_180)
    if not ret:
        print("未读取")
        break
    #切片
    x1, y1, x2, y2 = 200, 250, 270, 315
    roi = frame[y1:y2, x1:x2]
    #转化颜色空间
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV_FULL)
    #生成各颜色掩码
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
    mask_red = cv2.bitwise_or(
        cv2.inRange(hsv, lower_red1, upper_red1),
        cv2.inRange(hsv, lower_red2, upper_red2)
    )
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    #统计像素，判断状态
    purple_pixel_count = cv2.countNonZero(mask_purple)
    red_pixel_count = cv2.countNonZero(mask_red)
    blue_pixel_count = cv2.countNonZero(mask_blue)

    color_counts = {'red': red_pixel_count, 'blue': blue_pixel_count, 'purple': purple_pixel_count}
    max_color = max(color_counts.values())
    if max_color < 200:
        dominant_color = "nothing"
    else:
        dominant_color = max(color_counts, key=color_counts.get)
    #显示结果
    cv2.rectangle(frame,(x1, y1),(x2, y2),(0, 255, 0), 2)
    cv2.putText(frame, f"color:{dominant_color}", (50,50),
    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('frame',frame)
    cv2.waitKey(25)
cam.release()
cv2.destroyAllWindows()




