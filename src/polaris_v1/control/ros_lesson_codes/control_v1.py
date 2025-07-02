#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

def move_robot():
    # Initialize the ROS node
    rospy.init_node('robot_mover_and_servo_controller', anonymous=True)
    # Create a publisher to the /cmd_vel topic
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # Create publishers for servo positions
    fls_pub = rospy.Publisher('/FLS_Joint_position_controller/command', Float64, queue_size=10)
    frs_pub = rospy.Publisher('/FRS_Joint_position_controller/command', Float64, queue_size=10)
    bls_pub = rospy.Publisher('/BLS_Joint_position_controller/command', Float64, queue_size=10)
    brs_pub = rospy.Publisher('/BRS_Joint_position_controller/command', Float64, queue_size=10)
    joints = ["FLS_Joint_position_controller", "FRS_Joint_position_controller", "BLS_Joint_position_controller","BRS_Joint_position_controller"]
    pub = []
    for jointName in joints:
        path = "/"+jointName+"/command" 
        x = rospy.Publisher(path, Float64, queue_size=10)
        pub.append(x)
    
    # Set the rate at which to publish messages
    rate = rospy.Rate(10)  # 10 Hz
    
    # Create a Twist message and set the linear and angular velocities
    vel_msg = Twist()
 
    # Create a Float message and set the wheel position
    fls_pos_msg = Float64()
    frs_pos_msg = Float64()
    bls_pos_msg = Float64()
    brs_pos_msg = Float64()
    
    # Example: Move forward with linear velocity of 1.5 m/s
    vel_msg.linear.x = 1.5
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    # Example: Rotate with angular velocity of 0.0 rad/s
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = -0.1  
    x=0
    # Example positions for servos
    fls_pos_msg.data = x
    frs_pos_msg.data = x
    bls_pos_msg.data = x
    brs_pos_msg.data = x
    rospy.loginfo("Moving the robot...")
    # Publish the velocity commands and servo positions for a certain duration
    duration = 5 # Move for 10 seconds
    start_time = rospy.Time.now().to_sec()
    
    while rospy.Time.now().to_sec() - start_time < duration:
    
      # Publish the velocity message
      velocity_publisher.publish(vel_msg)
        
      # Publish servo positions
      fls_pub.publish(fls_pos_msg)
      frs_pub.publish(frs_pos_msg)
      bls_pub.publish(bls_pos_msg)
      brs_pub.publish(brs_pos_msg)
              
      # Sleep for the remaining time until we hit the rate
      rate.sleep()
      
    # Stop the robot after the duration
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
        
    fls_pos_msg.data = 0.0
    frs_pos_msg.data = 0.0
    bls_pos_msg.data = 0.0
    brs_pos_msg.data = 0.0
        
    velocity_publisher.publish(vel_msg)   
        
    fls_pub.publish(fls_pos_msg)  
    bls_pub.publish(bls_pos_msg)  
    frs_pub.publish(frs_pos_msg)  
    brs_pub.publish(brs_pos_msg)  
        
    rospy.loginfo("Robot stopped.")      
    
if __name__ == '__main__':
    try:
        move_robot()     
    except rospy.ROSInterruptException:
        pass


