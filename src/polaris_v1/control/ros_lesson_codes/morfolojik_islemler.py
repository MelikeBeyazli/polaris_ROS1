#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Morfolojik İşlemler
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
        rospy.Subscriber("camera/rgb/image_raw",Image,self.kameraCallback)
        rospy.spin()
        
    def kameraCallback(self,mesaj):
        img = self.bridge.imgmsg_to_cv2(mesaj,"mono8")
        ret,esiklenmis = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
        kernel = np.ones((11,11),np.uint8)
        e_img = cv2.erode(esiklenmis,kernel)
        d_img = cv2.dilate(esiklenmis,kernel)
        f_img = d_img - e_img
        o_img = cv2.morphologyEx(esiklenmis,cv2.MORPH_OPEN,kernel)
        c_img = cv2.morphologyEx(esiklenmis,cv2.MORPH_CLOSE,kernel)
        cv2.imshow("Robot Kamerasi",img)
        cv2.imshow("Esiklenmis",esiklenmis)
        cv2.imshow("Erosion",e_img)
        cv2.imshow("Dilation",d_img)
        cv2.imshow("Morfolojik Gradyan",f_img)
        cv2.imshow("Opening",o_img)
        cv2.imshow("Closing",c_img)
        cv2.waitKey(1)

Kamera()