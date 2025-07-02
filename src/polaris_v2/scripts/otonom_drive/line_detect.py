import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera


class LineFollower:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        
    def process_frame(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Siyah çizgi için maske oluşturma
        down_black = np.array([0, 0, 0])
        top_black = np.array([180, 255, 30])
        maske = cv2.inRange(hsv, down_black, top_black)
        sonuc = cv2.bitwise_and(img, img, mask=maske)

        # Görüntü merkezi
        h, w, d = img.shape
        center_x, center_y = w // 2, h // 2

        # Maske üzerinde moment hesaplama
        M = cv2.moments(maske)

        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            sapma = cx - center_x
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), -1)

            # Yol ayrımını tespit etme
            left_half = maske[:, :center_x]
            right_half = maske[:, center_x:]
            left_sum = np.sum(left_half)
            right_sum = np.sum(right_half)
            return -sapma/100
        else:
            print("Çizgi bulunamadı")
            # Çizgi bulunamadığında ne yapılacağını ekleyebilirsiniz
            return None

        cv2.imshow("Orjinal", img)
        cv2.waitKey(1)

        
    def kameraCallback(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            img = frame.array
            self.process_frame(img)
            self.rawCapture.truncate(0)

