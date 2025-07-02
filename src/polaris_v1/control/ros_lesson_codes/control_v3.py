#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from math import pi
import time
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
    
    # Set the rate at which to publish messages
    rate = rospy.Rate(10)  # 10 Hz
    
    # Create a Twist message and set the linear and angular velocities
    vel_msg = Twist()

    # Create a Float message and set the wheel position
    fls_pos_msg = Float64()
    frs_pos_msg = Float64()
    bls_pos_msg = Float64()
    brs_pos_msg = Float64()
    
    def move_forward():    
      # Example: Move forward with linear velocity of 1.5 m/s
      vel_msg.linear.x = 0.5
      vel_msg.linear.y = 0
      vel_msg.linear.z = 0
      # Example: Rotate with angular velocity of 0.0 rad/s
      vel_msg.angular.x = 0
      vel_msg.angular.y = 0
      vel_msg.angular.z = 0  
      x=0
      # Example positions for servos
      fls_pos_msg.data = x
      frs_pos_msg.data = x
      bls_pos_msg.data = x
      brs_pos_msg.data = x
      
    def move_back():    
      # Example: Move forward with linear velocity of 1.5 m/s
      vel_msg.linear.x = -0.5
      vel_msg.linear.y = 0
      vel_msg.linear.z = 0
      # Example: Rotate with angular velocity of 0.0 rad/s
      vel_msg.angular.x = 0
      vel_msg.angular.y = 0
      vel_msg.angular.z = 0  
      x=0
      # Example positions for servos
      fls_pos_msg.data = x
      frs_pos_msg.data = x
      bls_pos_msg.data = x
      brs_pos_msg.data = x
      
    def turn_right():    
      # Example: Move forward with linear velocity of 1.5 m/s
      vel_msg.linear.x = 0.5
      vel_msg.linear.y = 0
      vel_msg.linear.z = 0
      # Example: Rotate with angular velocity of 0.0 rad/s
      vel_msg.angular.x = 0
      vel_msg.angular.y = 0
      vel_msg.angular.z = 0  
      x=(30/180)*3.14
      # Example positions for servos
      fls_pos_msg.data = x
      frs_pos_msg.data = x
      bls_pos_msg.data = x
      brs_pos_msg.data = x
      
    def turn_left():    
      # Example: Move forward with linear velocity of 1.5 m/s
      vel_msg.linear.x = 0.5
      vel_msg.linear.y = 0
      vel_msg.linear.z = 0
      # Example: Rotate with angular velocity of 0.0 rad/s
      vel_msg.angular.x = 0
      vel_msg.angular.y = 0
      vel_msg.angular.z = 0  
      x=-(30/180)*3.14
      # Example positions for servos
      fls_pos_msg.data = x
      frs_pos_msg.data = x
      bls_pos_msg.data = x
      brs_pos_msg.data = x 
    def stop():
      # Stop the robot after the duration
      vel_msg.linear.x = 0
      vel_msg.angular.z = 0
        
      fls_pos_msg.data = 0.0
      frs_pos_msg.data = 0.0
      bls_pos_msg.data = 0.0
      brs_pos_msg.data = 0.0
    
    rospy.loginfo("Moving the robot...")
    # Publish the velocity commands and servo positions for a certain duration
    duration = 15 # Move for 10 seconds
    
    
    while True:
      msj= input("w:Düz ilerle, s:Ters git, a:Sola 15 derece açı ile git, d:Sağa 15 derece açı ile git, b:Dur\nKomut gir:")
      start_time = rospy.Time.now().to_sec()
      if msj == "w" or msj == "W":
        move_forward()     
        # Publish the velocity message
        velocity_publisher.publish(vel_msg)
 
        # Publish servo positions
        fls_pub.publish(fls_pos_msg)
        frs_pub.publish(frs_pos_msg)
        bls_pub.publish(bls_pos_msg)
        brs_pub.publish(brs_pos_msg)
        if rospy.Time.now().to_sec() - start_time == 5:
          # Sleep for the remaining time until we hit the rate
          stop()
          rate.sleep()
      elif msj == "s" or msj == "S":
        move_back()     
        # Publish the velocity message
        velocity_publisher.publish(vel_msg)
 
        # Publish servo positions
        fls_pub.publish(fls_pos_msg)
        frs_pub.publish(frs_pos_msg)
        bls_pub.publish(bls_pos_msg)
        brs_pub.publish(brs_pos_msg)
        if rospy.Time.now().to_sec() - start_time == 5:
          # Sleep for the remaining time until we hit the rate
          stop()
          rate.sleep()
      elif msj == "w" or msj == "W":
        move_back()     
        # Publish the velocity message
        velocity_publisher.publish(vel_msg)
 
        # Publish servo positions
        fls_pub.publish(fls_pos_msg)
        frs_pub.publish(frs_pos_msg)
        bls_pub.publish(bls_pos_msg)
        brs_pub.publish(brs_pos_msg)
        if rospy.Time.now().to_sec() - start_time == 5:
          # Sleep for the remaining time until we hit the rate
          stop()
          rate.sleep()
          
      elif msj == "a" or msj == "A":
        turn_left()     
        # Publish the velocity message
        velocity_publisher.publish(vel_msg)
 
        # Publish servo positions
        fls_pub.publish(fls_pos_msg)
        frs_pub.publish(frs_pos_msg)
        bls_pub.publish(bls_pos_msg)
        brs_pub.publish(brs_pos_msg)
        if rospy.Time.now().to_sec() - start_time == 2:
          stop()
          # Sleep for the remaining time until we hit the rate
          rate.sleep()
          
      elif msj == "d" or msj == "D":
        turn_right()     
        # Publish the velocity message
        velocity_publisher.publish(vel_msg)
 
        # Publish servo positions
        fls_pub.publish(fls_pos_msg)
        frs_pub.publish(frs_pos_msg)
        bls_pub.publish(bls_pos_msg)
        brs_pub.publish(brs_pos_msg)
        if rospy.Time.now().to_sec()- start_time == 2:
          # Sleep for the remaining time until we hit the rate
          stop()
          rate.sleep()
      elif msj == "b" or msj == "B":
        stop()     
        # Publish the velocity message
        velocity_publisher.publish(vel_msg)
 
        # Publish servo positions
        fls_pub.publish(fls_pos_msg)
        frs_pub.publish(frs_pos_msg)
        bls_pub.publish(bls_pos_msg)
        brs_pub.publish(brs_pos_msg)
        #if rospy.Time.now().to_sec() - start_time > 2:
        rospy.loginfo("Robot stopped.") 
        # Sleep for the remaining time until we hit the rate
        rate.sleep()                
    
if __name__ == '__main__':
    try:
        move_robot()     
    except rospy.ROSInterruptException:
        pass

