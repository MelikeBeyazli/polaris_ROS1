#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uygulama 6: Lazer Sensörden Gelen Veriyi Kullanma
"""

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class LazerVerisi():
    def __init__(self):
        rospy.init_node("lazer_dugumu")
        self.pub = rospy.Publisher("cmd_vel",Twist,queue_size = 10)
        self.hiz_mesaji = Twist()
        rospy.Subscriber("scan",LaserScan,self.lazerCallback)  # lazerden gelen veriye abone
        rospy.spin()
    
    def lazerCallback(self,mesaj):
        """
           aracın orjin olarak alırsak ön verilerde 0 ile 90 arasındaki veriler mesaj.ranges[0:9] iken 0 ile 270 arasındaki veriler mesaj.ranges[350:359]
           olur. bu durumda aracın ön mesafe verileri iki matrisin eklenmesi ile oluşmakadır aynı mantık yanlar ve arka içinde geçerli.
           gelen bu verilerden min değeri alanarak nesne tespiti yapılmakta.
                      0
                      |
                      |
                      |
       90   _________ o __________ 270  
                      | 
                      |
                      | 
                    180
        """
        sol_on = list(mesaj.ranges[0:9]) 
        sag_on = list(mesaj.ranges[350:359])
        on = sol_on + sag_on
        sol = list(mesaj.ranges[80:100])
        sag = list(mesaj.ranges[260:280])
        arka = list(mesaj.ranges[170:190])
        min_on = min(on)
        min_sol = min(sol)
        min_sag = min(sag)
        min_arka = min(arka)
        print(min_on,min_sol,min_sag,min_arka)
        if min_on < 1.0: # aracın mesafesi 1 den azsa durdur değilse ilerlemeye devam et.
            self.hiz_mesaji.linear.x = 0.0
            self.pub.publish(self.hiz_mesaji)
        else:
            self.hiz_mesaji.linear.x = 0.25
            self.pub.publish(self.hiz_mesaji)

nesne = LazerVerisi()