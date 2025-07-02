#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 00:16:37 2024

@author: mb
"""

from line_detect import LineFollower
from lidar_ile_mesafe import engel_tespit
from get_pwm import set_motor_speed, calculate_wheel_speeds_pwm
import rospy
import time

def velocity_analysis(v0, v1, x0, x1):
    delta_x = (x1 - x0) / 100
    a = (v1**2 - v0**2) / (2 * delta_x)
    t = (v1 - v0) / a
    return a, t

def etrafindan_dolan():
    # Aracı durdur
    set_motor_speed(1500, 1500)
    time.sleep(1)
    
    # Sağa dön (sol motor geri, sağ motor ileri)
    set_motor_speed(1800, 1200)
    time.sleep(1.5)  # Bu süreyi aracın sağa dönme yeteneğine göre ayarlayacağız
    
    # İleri hareket et
    set_motor_speed(1800, 1800)
    time.sleep(2)  # Bu süreyi aracın engelin yanından geçmesi için ayarlayacağız
    
    # Sola dön (sol motor ileri, sağ motor geri)
    set_motor_speed(1200, 1800)
    time.sleep(1.5)  # Bu süreyi aracın sola dönme yeteneğine göre ayarlayacağız
    
    # İleri hareket et
    set_motor_speed(1800, 1800)
    time.sleep(2)  # Bu süreyi aracın engelden tamamen geçmesi için ayarlayacağız
    
    # Normal hıza geri dön
    set_motor_speed(1500, 1500)

if __name__ == "__main__":
    rospy.init_node('otonom')
    rate = rospy.Rate(10)  # 10 Hz
    
    follower = LineFollower()
    engel = engel_tespit()
    
    try:
        while not rospy.is_shutdown():
            img = follower.kameraCallback()
            W = follower.process_frame(img)
            
            if W is not None:
                v0 = 2
                left_speed_pwm, right_speed_pwm = calculate_wheel_speeds_pwm(v0, W)
                set_motor_speed(left_speed_pwm, right_speed_pwm)
                x0 = engel_tespit()
                
                if x0:  # Engel tespit edilirse
                    start_time = time.time()
                    a, t = velocity_analysis(v0, 0, x0, 0.15)
                    while True:
                        elapsed_time = time.time() - start_time  
                        if elapsed_time <= t:
                            v1 = v0 - a * elapsed_time
                            left_speed_pwm, right_speed_pwm = calculate_wheel_speeds_pwm(v1, W)
                            set_motor_speed(left_speed_pwm, right_speed_pwm)
                            
                            if v1 == 0 and x0 == 15:
                                wait_start_time = time.time()
                                
                                while time.time() - wait_start_time <= 15:
                                    left_speed_pwm, right_speed_pwm = calculate_wheel_speeds_pwm(v1, W)
                                    set_motor_speed(left_speed_pwm, right_speed_pwm)
                                    
                                if engel_tespit():
                                    etrafindan_dolan()
                                else:
                                    left_speed_pwm, right_speed_pwm = calculate_wheel_speeds_pwm(v0, W)
                                    set_motor_speed(left_speed_pwm, right_speed_pwm)
                                break
                        
                else:  # Engel tespit edilmezse
                    left_speed_pwm, right_speed_pwm = calculate_wheel_speeds_pwm(v0, W)
                    set_motor_speed(left_speed_pwm, right_speed_pwm)
        rate.sleep()

    except rospy.ROSInterruptException:
        pass
