#!/usr/bin/env python3


# hız bilgisini yayınla 
# yayınlanan hız bilgisi ile arduinoda abone ol  ve hız değerini yazdır.
# bunu dene  daha sonra  diff drive üzerine çalış 

import rospy
from std_msgs.msg import Float32
import time

def send_motor_commands():
    # ROS düğümünü başlat
    rospy.init_node('motor_control_node')
    pub = rospy.Publisher('motor_speed', Float32, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    # 2 saniye ileri
    pub.publish(Float32(255))  # 255 maksimum PWM değeri
    time.sleep(2)

    # 2 saniye bekle
    pub.publish(Float32(0))  # PWM değerini 0 yap
    time.sleep(2)

    # 2 saniye geri
    pub.publish(Float32(-255))  # Negatif değer motorun geri gitmesini sağlar
    time.sleep(2)

    # Motoru durdur
    pub.publish(Float32(0))

if __name__ == '__main__':
    try:
        send_motor_commands()
    except rospy.ROSInterruptException:
        pass

