#!/usr/bin/env python3
import math, time
from std_msgs.msg import Float64MultiArray, Bool, Int32MultiArray
import sensorData, rospy
from velocityControl.sensorData import encoder_data

# Araç parametreleri
L = 0.6  # Tekerlekler arası mesafe (m)
r = 0.085  # Tekerlek yarıçapı (m)
rpm = 230  # Devir/dk
i = 1 / 15  # Motor redüksiyon oranı

# Maksimum hızın hesaplanması
Vmax = (rpm / i) * ((2 * math.pi) / 60) * r

def constrain(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def calculate_acceleration_profiles(_v0, _v1, _x0, _x1, _teta_deg):
    _teta = math.radians(_teta_deg)  # Derece cinsinden verilen açıyı radian cinsine çevir
    omega = _teta / 100  # rad/s olarak alınıyor
    if _v1 != _v0:
        # İki nokta arasındaki mesafenin hesaplanması
        delta_x = math.sqrt((_x1[0] - _x0[0]) ** 2 + (_x1[1] - _x0[1]) ** 2)  # metre cinsinden yerdeğiştirme miktarı
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
            # Tekerlek hızları
            v_l = (2 * _v1 - omega * L) / 2  # sol tekerlek hızı
            v_r = (2 * _v1 + omega * L) / 2  # sağ tekerlek hızı
            # Yönleri belirleyin
            r_dir = v_r >= 0.0
            l_dir = v_l >= 0.0
            r_pwm = int(constrain((abs(v_r) / Vmax) * 255, 0, 255))
            l_pwm = int(constrain((abs(v_l) / Vmax) * 255, 0, 255))
            pwm_values = [r_pwm, l_pwm]
            dir_values = [r_dir, l_dir]
            #sensorData.motor_control(pwm_values, dir_values)
            print(f"v_l: {v_l}, l_dir: {dir_values[1]}, lpwm: {pwm_values[1]}" )
            print(f"v_r: {v_r}, r_dir: {dir_values[0]}, rpwm: {pwm_values[0]}")
    else:
        # Tekerlek hızları
        v_l = (2 * _v1 - omega * L) / 2  # sol tekerlek hızı
        v_r = (2 * _v1 + omega * L) / 2  # sağ tekerlek hızı
        # Yönleri belirleyin
        r_dir = v_r >= 0.0
        l_dir = v_l >= 0.0
        r_pwm = int(constrain((abs(v_r) / Vmax) * 1024, 0, 1024))
        l_pwm = int(constrain((abs(v_l) / Vmax) * 1024, 0, 1024))
        pwm_values = [r_pwm, l_pwm]
        dir_values = [r_dir, l_dir]
        # sensorData.motor_control(pwm_values, dir_values)
        print(f"v_l: {v_l}, l_dir: {dir_values[1]}, lpwm: {pwm_values[1]}")
        print(f"v_r: {v_r}, r_dir: {dir_values[0]}, rpwm: {pwm_values[0]}")


v0 = 0
v1 = 0
teta = 180
x0 = [4, 3]
x1 = [8, 6]
calculate_acceleration_profiles(_v0=v0, _v1=v1, _x0=x0, _x1=x1, _teta_deg=teta)