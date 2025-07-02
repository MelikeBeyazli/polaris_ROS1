#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uygulama 6: Lazer Sensörden Gelen Veriyi Kullanma
"""

import rospy
from sensor_msgs.msg import LaserScan

distance = None

def lazerCallback(data):
    global distance
    distance = data

def engel_tespit():

    """
           aracın orjin olarak alırsak ön verilerde 0 ile 90 arasındaki veriler mesaj.ranges[0:9] iken 0 ile 270 arasındaki veriler mesaj.ranges[350:359]
           olur. bu durumda aracın ön mesafe verileri iki matrisin eklenmesi ile oluşmakadır aynı mantık yanlar ve arka içinde geçerli.
           gelen bu verilerden min değeri alanarak nesne tespiti yapılmakta.
                      0
                      |
                      |
                      |
       90   _________ o __________ 270
                      |a
                      |
                      |
                    180
    """
    
    global distance
    rospy.Subscriber("scan", LaserScan, lazerCallback)
    
    if distance is not None:
        sol_on = list(distance.ranges[0:9])
        sag_on = list(distance.ranges[350:359])
        on = sol_on + sag_on
        sol = list(distance.ranges[80:100])
        sag = list(distance.ranges[260:280])
        arka = list(distance.ranges[170:190])
        min_on = min(on)
        min_sol = min(sol)
        min_sag = min(sag)
        min_arka = min(arka)
        print(min_on, min_sol, min_sag, min_arka)
        if min_on < 0.3:  # aracın mesafesi 0.3 m den azsa durdur değilse ilerlemeye devam et.
            print("Engel tespit edildi!")
            return True
        else:
            print("Engel yok, devam et.")
            return False
    else:
        rospy.logwarn("Mesafe verisi henüz mevcut değil.")
        return False



