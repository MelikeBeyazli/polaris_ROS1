#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class HedefeGit():
    def __init__(self):
        rospy.init_node("duz_git")
        self.hedef_konum = 20.0
        self.guncel_konum = 0.0
        self.kontrol = True
        rospy.Subscriber("odom", Odometry, self.odomCallback)  # Aracın orijine göre konumunu belirtir.
        pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        hiz_mesaji =Twist()
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            if self.kontrol:
                hiz_mesaji.linear.x = 0.5
                pub.publish(hiz_mesaji)
            else:
                hiz_mesaji.linear.x = 0.0
                pub.publish(hiz_mesaji)
                rospy.loginfo("Hedefe varildi !")
            rate.sleep()
        
    def odomCallback(self, mesaj):
        # print(mesaj.pose.pose.position.x)
        self.guncel_konum = mesaj.pose.pose.position.x
        if self.guncel_konum <= self.hedef_konum:
            self.kontrol = True
        else:
            self.kontrol = False
try:
    HedefeGit()
except rospy.ROSInterruptException:
    print("Dugum Sonlandı!!")

