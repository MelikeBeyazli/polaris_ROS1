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


if __name__ == '__main__':
    try:
        # Test verileri
        v0 = 10
        v1 = 15
        teta = 180
        x0 = [0, 0]
        x1 = [3, 16]

        # Test
        target = TargetSpeed()
        target.vehicle_speed(v0, v1, x0, x1, teta)
    except rospy.ROSInterruptException:
        pass
