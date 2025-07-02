#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kenar Bulma İşlemleri
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
        kenarlar = cv2.Canny(img,100,200,5)
        cv2.imshow("Robot Kamerasi",img)
        cv2.imshow("Canny Kenarlar",kenarlar)
        cv2.waitKey(1)

Kamera()