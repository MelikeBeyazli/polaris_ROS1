#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Range

# Initialize global variables for distance
distance_fr = None
distance_fl = None

def range_callback_fr(data):
    global distance_fr
    distance_fr = data.range

def range_callback_fl(data):
    global distance_fl
    distance_fl = data.range

def engel_tespit():
    
    rospy.init_node('ultrasound_listener', anonymous=True)
    
    # Subscribe to both distance sensors
    rospy.Subscriber("/FR_mesafe", Range, range_callback_fr)
    rospy.Subscriber("/FL_mesafe", Range, range_callback_fl)
    
    rate = rospy.Rate(10)  # 10 Hz 
    while not rospy.is_shutdown(): 
        if distance_fr is not None and distance_fl is not None:
            distance = (distance_fl+distance_fr)/2
            if distance <=30:
                rospy.loginfo("Engel tespit edildi! Mesafe: %.2f", distance)
                return True
            else:
                rospy.loginfo("Engel yok. Mesafe: %.2f", distance)
                return False
        else:
            rospy.logwarn("Mesafe verisi henüz mevcut değil.")
            return False
        rate.sleep()

