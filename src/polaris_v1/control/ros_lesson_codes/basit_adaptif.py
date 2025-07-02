#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basit ve Adaptif Eşikleme Yöntemleri
"""

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class Kamera():
    def __init__(self):
        rospy.init_node("kamera_dugumu")
        self.bridge = CvBridge()
        rospy.Subscriber("camera/rgb/image_raw",Image,self.kameraCallback)
        rospy.spin()
        
    def kameraCallback(self,mesaj):
        img = self.bridge.imgmsg_to_cv2(mesaj,"mono8")
        ret,esiklenmis = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        a_esiklenmis = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY,11,2)
        cv2.imshow("Robot Kamerasi",img)
        cv2.imshow("Basit Esikleme",esiklenmis)
        cv2.imshow("Adaptif Esikleme",a_esiklenmis)
        cv2.waitKey(1)

Kamera()