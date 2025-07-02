#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aritmetik İşlemler
"""

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class Kamera():
    def __init__(self):
        rospy.init_node("kamera_dugumu")
        self.bridge = CvBridge()
        rospy.Subscriber("camera_depth/color/image_raw",Image,self.kameraCallback)
        rospy.spin()
        
    def kameraCallback(self,mesaj):
        img = self.bridge.imgmsg_to_cv2(mesaj,"bgr8")
        kirmizi = cv2.imread("/home/mb/catkin_ws/src/star_v1/scripts/kirmizi.png")
        yeni_kirmizi = cv2.resize(kirmizi, (640,480))
        # print(img.shape)
        # print(kirmizi.shape)
        # print(yeni_kirmizi.shape)
        toplama = cv2.add(img,yeni_kirmizi)
        a_toplama = cv2.addWeighted(img,0.9,yeni_kirmizi,0.1,0)
        cikarma = cv2.subtract(yeni_kirmizi,img)
        cv2.imshow("Robot Kamerasi",img)
        cv2.imshow("Kırmızı Goruntu",yeni_kirmizi)
        cv2.imshow("Toplama",toplama)
        cv2.imshow("Agirlikli Toplama",a_toplama)
        cv2.imshow("Cikarma",cikarma)
        cv2.waitKey(1)

Kamera()