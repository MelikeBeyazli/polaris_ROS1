#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Range

distance = None

def range_callback(data):
    global distance
    distance = data.range

def listener():
    rospy.init_node('ultrasound_listener', anonymous=True)
    rospy.Subscriber("/FR_mesafe", Range, range_callback)
    rate = rospy.Rate(10)  # 10 Hz 

    while not rospy.is_shutdown():
        if distance is not None:
            if distance < 10:
                rospy.loginfo("Change the position, You're going to crush!!!!!")
            else:
                rospy.loginfo("You can move forward")
        else:
            rospy.logwarn("Distance data is not yet available.")
        rate.sleep()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass

