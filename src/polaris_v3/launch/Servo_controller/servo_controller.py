#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from control_msgs.msg import JointControllerState
from dynamic_reconfigure.server import Server
from your_package.cfg import PIDConfig  # PIDConfig dosyanızı buraya ekleyin

class PIDControllerNode:
    def __init__(self):
        rospy.init_node('pid_controller_node')

        # PID gains from parameter server
        self.p_gain = rospy.get_param('~p_gain', 100.0)
        self.i_gain = rospy.get_param('~i_gain', 1.0)
        self.d_gain = rospy.get_param('~d_gain', 10.0)

        # Publishers for each joint
        self.joint_publishers = {
            'FRS_Joint': rospy.Publisher('/FRS_Joint/command', Float64, queue_size=10),
            'FLS_Joint': rospy.Publisher('/FLS_Joint/command', Float64, queue_size=10),
            'BRS_Joint': rospy.Publisher('/BRS_Joint/command', Float64, queue_size=10),
            'BLS_Joint': rospy.Publisher('/BLS_Joint/command', Float64, queue_size=10)
        }

        # Dynamic reconfigure server
        self.srv = Server(PIDConfig, self.reconfigure_callback)

        rospy.loginfo("PID Controller Node Initialized")

    def reconfigure_callback(self, config, level):
        self.p_gain = config.p_gain
        self.i_gain = config.i_gain
        self.d_gain = config.d_gain
        rospy.loginfo("Reconfigured PID gains: p=%f, i=%f, d=%f", self.p_gain, self.i_gain, self.d_gain)
        return config

    def control_loop(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            # Implement your control logic here
            for joint, publisher in self.joint_publishers.items():
                command = Float64()
                command.data = self.calculate_command(joint)
                publisher.publish(command)
            rate.sleep()

    def calculate_command(self, joint_name):
        # Implement your PID control logic here
        # For simplicity, we'll just return a constant value
        return 0.0

if __name__ == '__main__':
    node = PIDControllerNode()
    node.control_loop()

