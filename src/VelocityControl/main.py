#!/usr/bin/env python3
import math, time
import rospy
from std_msgs.msg import Float64MultiArray, Bool, Int32MultiArray


class TargetSpeed:
    def __init__(self):
        self.wheelBase = 0.6  # Tekerlekler arası mesafe (m)
        self.wheelRadius = 0.085  # Tekerlek yarıçapı (m)
        self.motorRPM = 230  # Devir/dk
        self.R = 1 / 15  # Motor redüksiyon oranı
        self.vMax = (self.motorRPM / self.R) * ((2 * math.pi) / 60) * self.wheelRadius  # Maksimum hızın hesaplanması
        self.minPWM = 0
        self.maxPWM = 255

    def wheel_speed(self, _v1, omega):
        # Tekerlek hızları
        v_l = (2 * _v1 - omega * self.wheelBase) / 2  # sol tekerlek hızı
        v_r = (2 * _v1 + omega * self.wheelBase) / 2  # sağ tekerlek hızı
        # Yönleri belirleyin
        r_dir = v_r >= 0.0
        l_dir = v_l >= 0.0
        speed_values = [v_r, v_l]
        dir_values = [r_dir, l_dir]
        print(f"v_l: {speed_values[1]}, l_dir: {dir_values[1]}")
        print(f"v_r: {speed_values[0]}, r_dir: {dir_values[0]}")
        return speed_values, dir_values

    def constrain(self, value):
        value_ = int(abs((self.maxPWM * value) / self.vMax))
        return max(self.minPWM, min(value_, self.maxPWM))

    def send_speed(self, speed_values, dir_values):
        pwm_pub = rospy.Publisher('/pwm_topic', Int32MultiArray, queue_size=10)

        dir_pub_rf = rospy.Publisher('/RF_dir_topic', Bool, queue_size=10)
        dir_pub_lf = rospy.Publisher('/LF_dir_topic', Bool, queue_size=10)

        #rospy.init_node('target_speed_node')

        #        rate = rospy.Rate(10)  # 10 Hz

        pwm_msg = Int32MultiArray()
        dir_msg_rf = Bool()
        dir_msg_lf = Bool()

        r_pwm = self.constrain(speed_values[0])  # int(abs((self.maxPWM * speed_values[0]) / self.vMax))
        l_pwm = self.constrain(speed_values[1])  # int(abs((self.maxPWM * speed_values[1]) / self.vMax))

        pwm_values = [r_pwm, l_pwm]
        dir_values = dir_values

        print(f"lpwm: {pwm_values[1]}")
        print(f"rpwm: {pwm_values[0]}")

        # Motor PWM değerlerini ayarlayın
        pwm_msg.data = pwm_values  # Örnek PWM değerleri
        pwm_pub.publish(pwm_msg)

        # Motor yön değerlerini ayarlayın
        dir_msg_rf.data = dir_values[0]
        dir_msg_lf.data = dir_values[1]

        dir_pub_rf.publish(dir_msg_rf)
        dir_pub_lf.publish(dir_msg_lf)

    def vehicle_speed(self, _v0, _v1, _x0, _x1, _teta_deg):
        _teta = math.radians(_teta_deg)  # Derece cinsinden verilen açıyı radian cinsine çevir
        omega = _teta_deg / 100  # rad/s olarak alınıyor
        if _v1 != _v0:
            # İki nokta arasındaki mesafenin hesaplanması
            delta_x = math.sqrt((_x1[0] - _x0[0]) ** 2 + (_x1[1] - _x0[1]) ** 2)  # metre cinsinden yerdeğiştirme miktar
            _a = (_v1 ** 2 - _v0 ** 2) / (2 * delta_x)  # m/s^2 cinsinden ivme
            _t = abs(_v1 - _v0) / abs(_a)
            start_time = time.time()
            elapsed_time = time.time() - start_time
            _x = 0
            while elapsed_time <= _t:
                _v1 = _v0 + _a * elapsed_time
                _x = _v0 * elapsed_time + (_a * elapsed_time ** 2) / 2
                elapsed_time = time.time() - start_time
                print(f"v1:{_v1}  : t:{elapsed_time}  : x:{_x}")
                vel, dir_ = self.wheel_speed(_v1=_v1, omega=omega)
                self.send_speed(vel, dir_)
                return vel

        else:
            vel, dir_ = self.wheel_speed(_v1=_v1, omega=omega)
            self.send_speed(vel, dir_)
            return vel

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

class PIDController:
    def __init__(self):
        self.kp = 1.0
        self.ki = 0.0
        self.kd = 0.0
        self.integral_error = 0
        self.last_error = 0
        self.time_interval = 0.1

    def compute(self, error):
        self.integral_error += error * self.time_interval
        derivative_error = (error - self.last_error) / self.time_interval
        control_output = (self.kp * error) + (self.ki * self.integral_error) + (self.kd * derivative_error)
        self.last_error = error
        return control_output


if __name__ == '__main__':
    try:
        rospy.init_node('control_node')

        # Test verileri
        v0 = 15
        v1 = 15
        teta = 0
        x0 = [0, 0]
        x1 = [3, 16]

        # Sınıf örnekleri
        target = TargetSpeed()
        real = RealSpeed()
        PID = PIDController()

        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            # Hız hesaplama ve kontrol işlemleri
            target_speeds = target.vehicle_speed(v0, v1, x0, x1, teta)
            real_speeds = real.real_speed()

            # Hataları hesapla
            right_error = target_speeds[0] - real_speeds[0]
            left_error = target_speeds[1] - real_speeds[1]

            # PID kontrol işlemi
            right_control = PID.compute(right_error)
            left_control = PID.compute(left_error)

            target.send_speed([right_control, left_control], [right_control >= 0, left_control >= 0])

            rate.sleep()

    except rospy.ROSInterruptException:
        pass
