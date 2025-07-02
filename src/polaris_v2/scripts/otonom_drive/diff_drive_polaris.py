#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int16

def motor_control():
    pub = rospy.Publisher('motor_speed', Int16, queue_size=10)
    rospy.init_node('motor_controller', anonymous=True)
    rate = rospy.Rate(10)  # 10hz

    while not rospy.is_shutdown():
        speed = int(input("Motor hızı girin (-255 ile 255 arasında): "))
        rospy.loginfo(speed)
        pub.publish(speed)
        rate.sleep()

if __name__ == '__main__':
    try:
        motor_control()
    except rospy.ROSInterruptException:
        pass

