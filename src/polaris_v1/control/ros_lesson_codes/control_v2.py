#!/usr/bin/env python3
import math
import threading
import rospy
import numpy as np
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

vel_msg = Twist()  # robot velocity
mode_selection = 0  # 1: opposite phase, 2: in-phase, 3: pivot turn, 4: none

class Commander:

    def __init__(self):
        rospy.init_node('commander', anonymous=True)
        self.rate = rospy.Rate(50)  # 50 Hz
        self.wheel_base = 0.156  # l yerine geçer. sağ ön ve araka tekerlerin merkezleri arasındaki mesafe
        self.wheel_radius = 0.0625  # teker  yarıçapı
        self.steering_track = 300 # w yerine geçer. ön tekerlerin merkezleri arasındaki mesafe

        self.pos = np.zeros(4)
        self.vel = np.zeros(4)
        
        self.sub_joy = rospy.Subscriber('joy', Joy, self.joy_callback)
        
    def joy_callback(self, data):
        global vel_msg, mode_selection

        if data.buttons[0] == 1:  # in-phase: A button of Xbox 360 controller
            mode_selection = 2
        elif data.buttons[4] == 1:  # opposite phase: LB button of Xbox 360 controller
            mode_selection = 1
        elif data.buttons[5] == 1:  # pivot turn: RB button of Xbox 360 controller
            mode_selection = 3
        else:
            mode_selection = 4

        vel_msg.linear.x = data.axes[1] * 7.5
        vel_msg.linear.y = data.axes[0] * 7.5
        vel_msg.angular.z = data.axes[3] * 10

    def timer_callback(self):
        global vel_msg, mode_selection

        if mode_selection == 1:  # opposite phase
            vel_steering_offset = vel_msg.angular.z * self.wheel_steering_y_offset
            sign = np.sign(vel_msg.linear.x)

            self.vel[0] = sign*math.hypot(vel_msg.linear.x - vel_msg.angular.z*self.steering_track/2, vel_msg.angular.z*self.wheel_base/2) - vel_steering_offset
            self.vel[1] = sign*math.hypot(vel_msg.linear.x + vel_msg.angular.z*self.steering_track/2, vel_msg.angular.z*self.wheel_base/2) + vel_steering_offset
            self.vel[2] = sign*math.hypot(vel_msg.linear.x - vel_msg.angular.z*self.steering_track/2, vel_msg.angular.z*self.wheel_base/2) - vel_steering_offset
            self.vel[3] = sign*math.hypot(vel_msg.linear.x + vel_msg.angular.z*self.steering_track/2, vel_msg.angular.z*self.wheel_base/2) + vel_steering_offset

            self.pos[0] = math.atan(vel_msg.angular.z*self.wheel_base/(2*vel_msg.linear.x + vel_msg.angular.z*self.steering_track))
            self.pos[1] = math.atan(vel_msg.angular.z*self.wheel_base/(2*vel_msg.linear.x - vel_msg.angular.z*self.steering_track))
            self.pos[2] = -self.pos[0]
            self.pos[3] = -self.pos[1]

        elif mode_selection == 2:  # in-phase
            V = math.hypot(vel_msg.linear.x, vel_msg.linear.y)
            sign = np.sign(vel_msg.linear.x)
            
            if vel_msg.linear.x != 0:
                ang = vel_msg.linear.y / vel_msg.linear.x
            else:
                ang = 0
            
            self.pos[0] = math.atan(ang)
            self.pos[1] = math.atan(ang)
            self.pos[2] = self.pos[0]
            self.pos[3] = self.pos[1]
            
            self.vel[:] = sign * V

        elif mode_selection == 3:  # pivot turn
            self.pos[0] = -math.atan(self.wheel_base/self.steering_track)
            self.pos[1] = math.atan(self.wheel_base/self.steering_track)
            self.pos[2] = math.atan(self.wheel_base/self.steering_track)
            self.pos[3] = -math.atan(self.wheel_base/self.steering_track)
            
            self.vel[0] = -vel_msg.angular.z
            self.vel[1] = vel_msg.angular.z
            self.vel[2] = self.vel[0]
            self.vel[3] = self.vel[1]

        else:
            self.pos[:] = 0
            self.vel[:] = 0

        pos_array = Float64MultiArray(data=self.pos) 
        vel_array = Float64MultiArray(data=self.vel) 
        self.pub_pos.publish(pos_array)
        self.pub_vel.publish(vel_array)

    def start(self):
        while not rospy.is_shutdown():
            self.timer_callback()
            self.rate.sleep()

if __name__ == '__main__':
    try:
        commander = Commander()
        commander.start()
    except rospy.ROSInterruptException:
        pass


