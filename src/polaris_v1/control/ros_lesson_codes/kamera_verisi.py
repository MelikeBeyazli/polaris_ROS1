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
        self.foto = self.bridge.imgmsg_to_cv2(mesaj,"bgr8")  # gelen image mesajını çevir  bgr8(renkli görüntüye)
        cv2.imshow("Star_camera",self.foto)
        cv2.waitKey(1)

nesne = RobotKamera()
