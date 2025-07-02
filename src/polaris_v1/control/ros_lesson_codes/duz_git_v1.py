#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uygulama 1: Tek Eksen Boyunca Hareket I
"""
# Abone olmadan mesaj yayınlama işlemi yapılmaktadır
import rospy
from geometry_msgs.msg import Twist  
# Vector 3 Linear ve Anular olmak üzere iki mesaj bulunmakta her birinde ise float tipinde x, y, z hızları vardır

def hareket():
    rospy.init_node("duz_git")  # Düğümü başlatmak için kullanılır
    pub = rospy.Publisher("cmd_vel",Twist,queue_size=10)  # Yayıncı oluştur cmd_vel üzerinden
    hiz_mesaji = Twist()  # Hız mesajı oluştur
    hiz_mesaji.linear.x = 0.5  # x eksenindeki çizgisel hızını ayarla
    mesafe = 5
    yer_degistirme = 0
    t0 = rospy.Time.now().to_sec()
    while (yer_degistirme < mesafe):
        pub.publish(hiz_mesaji)  # hız mesajını yayınla
        t1 = rospy.Time.now().to_sec()
        yer_degistirme = hiz_mesaji.linear.x * (t1-t0) # yerdeğiştirme formülü (x=V.t)
    hiz_mesaji.linear.x = 0.0  # aracın görevini tamamladıktan sonra durması amacıyla hızını 0 yap
    pub.publish(hiz_mesaji)  # hız mesajını yayınla
    rospy.loginfo("Hedefe varildi !")  # Terminalde bilgi vermek amacıyla kullanılmakta

hareket()

