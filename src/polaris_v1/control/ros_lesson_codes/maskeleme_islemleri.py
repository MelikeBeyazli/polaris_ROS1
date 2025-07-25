#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maskeleme ve Bit Bazında İşlemler
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
        gri = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, maske = cv2.threshold(gri,50,255,cv2.THRESH_BINARY_INV)
        and_is = cv2.bitwise_and(img,img,mask=maske)
#        kirmizi = cv2.imread("/home/mb/catkin_ws/src/star_v1/scripts/kirmizi.png")
#        kirmizi = cv2.resize(kirmizi,(640,480))
#        print(img[0,0])
#        print(kirmizi[0,0])
#        and_is = cv2.bitwise_and(img,kirmizi)
#        or_is = cv2.bitwise_or(img,kirmizi)
#        xor_is = cv2.bitwise_xor(img,kirmizi)
#        not_is = cv2.bitwise_not(img)
#        print("-------------------")
#        print(and_is[0,0])
#        print(or_is[0,0])
#        print(xor_is[0,0])
#        print(not_is[0,0])
#        
        cv2.imshow("Robot Kamerasi",img)
        cv2.imshow("Maske",maske)
        cv2.imshow("Maskelenmis Goruntu",and_is)
        cv2.waitKey(1)

Kamera()