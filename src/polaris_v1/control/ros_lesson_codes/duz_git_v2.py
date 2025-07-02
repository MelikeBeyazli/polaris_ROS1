#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uygulama 2: Tek Eksen Boyunca Hareket II
"""

import rospy
from geometry_msgs.msg import Twist  # hız yayınlamak amacıyla
from nav_msgs.msg import Odometry  # komut bilgisini almak amacıyla odometry kullanılmaktadır.
from basit_uygulamalar.msg import Mesafe  
# Çalışma ortamınnda bulunan msg klasörüne Mesafe.msg isimli mesaj klasörü bulunmakta. 
# Bu dosayada float64 tipinde mesafe isimli bir mesaj tanımla. Bu mesajı CMakeLists.txt dosyasına eklemeyi unutma 
class HedefeGit():
    def __init__(self):
        rospy.init_node("duz_git")  # düğüm oluştur
        self.hedef_konum = 0.0
        self.guncel_konum = 0.0
        self.kontrol = True
        rospy.Subscriber("odom",Odometry,self.odomCallback)  # Yayınlanacak olan odom konusuna abone ol
        # rospy.spin()  # sürekli bunu döndür
        rospy.Subscriber("mesafe_git",Mesafe,self.mesafeCallback)
        pub = rospy.Publisher("cmd_vel",Twist,queue_size=10)  # yayaıcı oluştur cmd_vel konusu için
        hiz_mesaji = Twist()
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():  # CTRL+C ile terminali kapatmak için kullanılıyor olabilir????
            if self.kontrol:
                hiz_mesaji.linear.x = 0.5
                pub.publish(hiz_mesaji)
            else:
                hiz_mesaji.linear.x = 0.0
                pub.publish(hiz_mesaji)
                rospy.loginfo("Hedefe varildi !")
            rate.sleep()
        
    def odomCallback(self,mesaj):
        # print(mesaj.pose.pose.position.x)  # odom'dan gelen verileri incelemek amacıyla
        self.guncel_konum = mesaj.pose.pose.position.x
        if self.guncel_konum <= self.hedef_konum:
            self.kontrol = True
        else:
            self.kontrol = False

    def mesafeCallback(self,mesaj):
        self.hedef_konum = mesaj.mesafe
try:
    HedefeGit()
except rospy.ROSInterruptException:
    print("Dugum sonlandi!!!")