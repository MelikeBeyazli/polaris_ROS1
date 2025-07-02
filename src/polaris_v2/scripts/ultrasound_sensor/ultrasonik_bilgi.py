#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Range

# Initialize global variables for distance
distance_fr = None


def range_callback_fr(data):
    global distance_fr
    distance_fr = data.range


def engel_tespit():
    # Subscribe to both distance sensors
    rospy.Subscriber("/FR_mesafe", Range, range_callback_fr)
    if distance_fr is not None:
        distance = (distance_fr)
        if distance <= 30:
            msg = "Engel tespit edildi!"
            return distance, msg
        else:
            msg = "Engel yok"
            return False, msg
    else:
        msg = "Mesafe verisi henüz mevcut değil."
        return False, msg
