#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geometrik Dönüşümler: Afin, Perspektif
"""

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import numpy as np

class Kamera():
    def __init__(self):
        rospy.init_node("kamera_dugumu")
        self.bridge = CvBridge()
        rospy.Subscriber("camera_depth/color/image_raw",Image,self.kameraCallback)
        rospy.spin()
        
    def kameraCallback(self,mesaj):
        img = self.bridge.imgmsg_to_cv2(mesaj,"bgr8")
#        k1 = np.float32([[30,500],[200,500],[30,600]])
#        k2 = np.float32([[15,250],[100,250],[15,300]])
#        M = cv2.getAffineTransform(k1,k2)
#        afin = cv2.warpAffine(img,M,(640,480))
        cv2.imshow("Robot Kamerasi",img)
#        cv2.imshow("Afin Donusum",afin)
        k1 = np.float32([[5,250],[605,250],[5,400],[605,400]])
        k2 = np.float32([[0,0],[640,0],[0,480],[640,480]])
        M = cv2.getPerspectiveTransform(k1,k2)
        perspektif = cv2.warpPerspective(img,M,(640,480))
        cv2.imshow("Perspektif Donusum",perspektif)
        cv2.waitKey(1)

Kamera()