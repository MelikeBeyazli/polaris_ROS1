#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uygulama 3: Çember Boyunca Hareket - İstemci Düğümü
"""

import rospy
from basit_uygulamalar.srv import CemberHareket

rospy.wait_for_service("cember_servis")
try:
    yaricap = float(input("Yaricap giriniz: "))  # yarıçap değerini kullanıcıdan al
    servis = rospy.ServiceProxy("cember_servis",CemberHareket)
    servis(yaricap)  # servise kullanıcıdan alanıan değeri istek olarak ayarla
except rospy.ServiceException:
    print("Servisle alakali hata meydana geldi !!!")