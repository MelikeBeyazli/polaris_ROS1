#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
class LineFollower():
    def __init__(self):
        rospy.init_node("LineFollower_node")
        self.bridge = CvBridge()
        rospy.Subscriber("/camera_depth/color/image_raw",Image,self.kameraCallback)
        self.pub = rospy.Publisher("cmd_vel",Twist,queue_size = 10)
        self.hiz_mesaji = Twist()
        rospy.spin()
        
    def kameraCallback(self,mesaj):
        img = self.bridge.imgmsg_to_cv2(mesaj,"bgr8")
        #img = img[:,240:360,:]  # h w d
       
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        
        down_black = np.array([0,0,0])
        top_black = np.array([180,255,30])
        
        maske = cv2.inRange(hsv,down_black,top_black)
        
        sonuc = cv2.bitwise_and(img,img,mask=maske)
        
        h,w,d = img.shape
        cv2.circle(img,(int(w/2),int(h/2)),5,(0,0,255),-1)
        M = cv2.moments(maske)
        
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(img,(cx,cy),5,(255,0,0),-1)
            sapma = cx - w/2
            print(sapma)
            self.hiz_mesaji.linear.x = 1
            self.hiz_mesaji.angular.z = -sapma/100
            self.pub.publish(self.hiz_mesaji)
        else:
            self.hiz_mesaji.linear.x = 0.0
            self.hiz_mesaji.angular.z = 0.0
            self.pub.publish(self.hiz_mesaji)
            
        cv2.imshow("Orjinal",img)
        #cv2.imshow("Maske",maske)
        #cv2.imshow("Sonuc",sonuc)
        cv2.waitKey(1)
        
LineFollower()
