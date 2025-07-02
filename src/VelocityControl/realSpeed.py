#!/usr/bin/env python3
import math, time
import rospy
from std_msgs.msg import Float64MultiArray, Bool, Int32MultiArray

class RealSpeed:
    def __init__(self):
        # Başlangıçta gerekli değişkenleri tanımlayın
        self.right_encoder_data = 0
        self.left_encoder_data = 0
        self.wheelRadius = 0.085  # Tekerlek çapı (m)
        self.encoder_resolution = 1000  # Encoder çözünürlüğü (pulse per revolution)
        self.time_interval = 0.1  # Zaman aralığı (saniye)

        # ROS düğümünü başlat
        #rospy.init_node('real_speed_node')



    def encoder_callback(self, msg):  # 2 adet encoder bulunmaktadır
        if len(msg.data) > 2 :
            self.right_encoder_data = msg.data[0]
            self.left_encoder_data = msg.data[1]
        else:
            self.right_encoder_data = 500
            self.left_encoder_data = 500

        rospy.loginfo("Sağ Encoder Verileri: %s", self.right_encoder_data)
        rospy.loginfo("Sol Encoder Verileri: %s", self.left_encoder_data)

    def imu_callback(self):
        # Gerçek ivme verilerini almak için IMU'dan veri alınması gerekiyor
        # Örnek ivme değeri (m/s^2)
        return 0.01

    def real_speed(self):
        # Encoder verilerini almak için abone ol
        rospy.Subscriber('/encoder', Float64MultiArray, self.encoder_callback)

        # Encoder verilerini al ve hızı hesapla
        right_pulse_count = self.right_encoder_data
        left_pulse_count = self.left_encoder_data

        right_encoder_speed = (right_pulse_count * 3.14 * self.wheelRadius) / (self.encoder_resolution * self.time_interval)
        left_encoder_speed = (left_pulse_count * 3.14 * self.wheelRadius) / (self.encoder_resolution * self.time_interval)

        # IMU'dan ivme verisini al
        acceleration_x = self.imu_callback()

        # IMU'dan alınan ivme ile hız değişimini hesapla ve ekle
        imu_speed_contribution = acceleration_x * self.time_interval

        # Sol ve sağ tekerlek hızlarını ve IMU'nun katkısını birleştir
        right_current_speed = right_encoder_speed + imu_speed_contribution
        left_current_speed = left_encoder_speed + imu_speed_contribution
        vel = [right_current_speed, left_current_speed]
        rospy.loginfo("Sağ Motor Hızı: %f", right_current_speed)
        rospy.loginfo("Sol Motor Hızı: %f", left_current_speed)
        return vel
