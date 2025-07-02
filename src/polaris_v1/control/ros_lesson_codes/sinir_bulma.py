#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sınırlar ve Özellikleri
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
        img2 = self.bridge.imgmsg_to_cv2(mesaj,"bgr8")
        ret,esiklenmis = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
        sinirlar,hiyerarsi = cv2.findContours(esiklenmis,cv2.RETR_LIST,
                                              cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img2,sinirlar,-1,(0,255,0),5)
        cnt = sinirlar[0]
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(img2,(cx,cy),5,(255,255,255),-1)
        sol = tuple(cnt[cnt[:,:,0].argmin()][0])
        sag = tuple(cnt[cnt[:,:,0].argmax()][0])
        ust = tuple(cnt[cnt[:,:,1].argmin()][0])
        alt = tuple(cnt[cnt[:,:,1].argmax()][0])
        
        (x,y), r = cv2.minEnclosingCircle(cnt)
        merkez = (int(x),int(y))
        r = int(r)
        cv2.circle(img2,merkez,r,(255,0,0),2)
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.imshow("Robot Kamerasi",img2)
        cv2.waitKey(1)

Kamera()