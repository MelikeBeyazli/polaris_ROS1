#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uygulama 5: Kameradan Gelen Veriyi Görüntüye Çevirme
"""

import rospy
from sensor_msgs.msg import Image  # kameradan gelen bilgileri almak için
from cv_bridge import CvBridge  # gelen görüntüyü opencvye çevirecek köprü için 
import cv2

class RobotKamera():
    def __init__(self):
        rospy.init_node("kamera")  # düğüm oluştur.
        rospy.Subscriber("/camera_depth/color/image_raw",Image,self.kameraCallback)  # yayıncı oluştur
        self.bridge = CvBridge()  # köprü oluştur
        rospy.spin()
    
    def kameraCallback(self,mesaj):
        foto = self.bridge.imgmsg_to_cv2(mesaj,"bgr8")  # gelen image mesajını çevir  bgr8(renkli görüntüye)
        # foto2 = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)  # gelen renkli resimleri siyah beyaz yap
        # foto3 = cv2.cvtColor(foto, cv2.COLOR_BGR2HSV)  # hsv renk dönüşümü yap
        # cv2.imshow("Star_rgb_camera",foto)
        # cv2.imshow("Star_gray_camera",foto2)
        # cv2.imshow("Star_hsv_camera",foto3)
        b, g, r = cv2.split(foto)
        cv2.imshow("Star_rgb_camera",foto)
        cv2.imshow("Star_b_camera",b)
        cv2.imshow("Star_g_camera",g)
        cv2.imshow("Star_r_camera",r)        
        cv2.waitKey(1)

nesne = RobotKamera()