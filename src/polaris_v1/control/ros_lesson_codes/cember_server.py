#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uygulama 3: Çember Boyunca Hareket - Server Düğümü
"""

import rospy
from geometry_msgs.msg import Twist
from basit_uygulamalar.srv import CemberHareket  # servis klasoründe oluşturarak yarıçapı flaot64 olarak ekle.Dosyayı CMakelists.txt'e kelemyi unutma

def cemberFonksiyonu(istek):  # gelen istek doğrultusunda robotyun hareketini 
    hiz_mesaji = Twist()
    lineer_hiz = 0.5
    hiz_mesaji.linear.x = lineer_hiz
    yaricap = istek.yaricap
    # w = v / r | V = W.r
    hiz_mesaji.angular.z = lineer_hiz / yaricap
    while not rospy.is_shutdown():
        pub.publish(hiz_mesaji)

rospy.init_node("cember_hareket")
pub = rospy.Publisher("cmd_vel",Twist,queue_size=10)
rospy.Service("cember_servis",CemberHareket,cemberFonksiyonu)
rospy.spin()