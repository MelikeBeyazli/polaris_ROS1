#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import pygame
from nav_msgs.msg import Odometry

# Global variables to store the odometry data
linear_velocity = None
angular_velocity = None
position = None
orientation = None


def odom_callback(data):
    global linear_velocity, angular_velocity, position, orientation

    # Update global variables with the odometry data
    linear_velocity = data.twist.twist.linear
    angular_velocity = data.twist.twist.angular
    position = data.pose.pose.position
    orientation = data.pose.pose.orientation


def move_robot():

    # Initialize the ROS node
    rospy.init_node('robot_controller', anonymous=True)

    # Create a publisher to the /cmd_vel topic
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # Create publishers for servo positions
    fls_pub = rospy.Publisher(
        '/FLS_Joint_position_controller/command', Float64, queue_size=10)
    frs_pub = rospy.Publisher(
        '/FRS_Joint_position_controller/command', Float64, queue_size=10)
    bls_pub = rospy.Publisher(
        '/BLS_Joint_position_controller/command', Float64, queue_size=10)
    brs_pub = rospy.Publisher(
        '/BRS_Joint_position_controller/command', Float64, queue_size=10)

    # Abone olun /odom konuya
    rospy.Subscriber('/odom', Odometry, odom_callback)

    rate = rospy.Rate(10)  # 10 Hz # Set the rate at which to publish messages

    vel_msg = Twist()  # Create a Twist message and set the linear and angular velocities

    # Create a Float message and set the wheel position
    fls_pos_msg = Float64()
    frs_pos_msg = Float64()
    bls_pos_msg = Float64()
    brs_pos_msg = Float64()
    x = 0
    y = 0
    pygame.init()  # Pygame'i başlat
    display_surface = pygame.display.set_mode((600, 338))
    pygame.display.set_caption("Araç Kontrolü")

    imp = pygame.image.load("/home/melike/Pictures/about_control.png")

    font = pygame.font.SysFont('freesanbold.ttf', 14)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display_surface.fill((255, 255, 255))

        display_surface.blit(imp, (0, 0))

        # Odometry bilgilerini göster
        if linear_velocity and angular_velocity and position and orientation:
            text = font.render("Görev Başladı...", True, (0, 0, 0))
            velocity_text = font.render(
                f"Hız(m/s): {linear_velocity.x:.2f}", True, (0, 0, 0))
            angular_text = font.render(
                f"Açısal Hız(rad/s): {angular_velocity.z:.2f}", True, (0, 0, 0))
            position_text = font.render(
                f"Konum(m): x: {position.x:.2f}, y: {position.y:.2f}, z: {position.z:.2f}", True, (0, 0, 0))
            orientation_text = font.render(
                f"Yönelim(rad): z: {orientation.z:.2f}, w: {orientation.w:.2f}", True, (0, 0, 0))

            display_surface.blit(text, (370, 140))
            display_surface.blit(velocity_text, (370, 170))
            display_surface.blit(angular_text, (370, 200))
            display_surface.blit(position_text, (370, 230))
            display_surface.blit(orientation_text, (370, 260))

        # Ekranı güncelleyin
        pygame.display.flip()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            vel_msg.angular.z = 0.5  # Rotate with angular velocity of 0.1 rad/s
        elif keys[pygame.K_RIGHT]:
            vel_msg.angular.z = -0.5  # Rotate with angular velocity of -0.1 rad/s
        else:
            vel_msg.angular.z = 0  # Rotate with angular velocity of 0.1 rad/s

        if keys[pygame.K_UP]:
            vel_msg.linear.x = 0.5 # Move forward with linear velocity of 0.5 m/s
            if keys[pygame.K_SPACE]:
                vel_msg.linear.x += 0.1
            else:
                vel_msg.linear.x = 0.5 

        elif keys[pygame.K_DOWN]:
            vel_msg.linear.x = -0.5  # Move back with linear velocity of 0.5 m/s
            if keys[pygame.K_SPACE]:
                vel_msg.linear.x -= 0.1
            else:
                vel_msg.linear.x = -0.5 
        else:
            vel_msg.linear.x = 0  # Move back with linear velocity of 0.5 m/s

        if keys[pygame.K_a]:  # sola dönder servoyu
            x -= 0.1
            y -= 0.1

        elif keys[pygame.K_d]:  # sağa dönder servoyu
            x += 0.1
            y += 0.1

        elif keys[pygame.K_s]:  # döndür
            x = 0
            y = 0

        # positions for servos
        fls_pos_msg.data = x
        frs_pos_msg.data = y
        bls_pos_msg.data = y
        brs_pos_msg.data = x

        velocity_publisher.publish(vel_msg)  # Publish the velocity message

        # Publish servo positions
        fls_pub.publish(fls_pos_msg)
        frs_pub.publish(frs_pos_msg)
        bls_pub.publish(bls_pos_msg)
        brs_pub.publish(brs_pos_msg)

        rate.sleep()  # Sleep for the remaining time until we hit the rate


if __name__ == '__main__':
    try:
        move_robot()
    except rospy.ROSInterruptException:
        pass
