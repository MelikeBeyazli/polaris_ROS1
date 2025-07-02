from pymavlink import mavutil
import time

# ArduPilot'a bağlanmak için bağlantı kurun
connection_string = '/dev/ttyACM0'  # Bağlantı noktası
baud_rate = 57600                   # Baud hızı

# MAVLink bağlantısını başlat
master = mavutil.mavlink_connection(connection_string, baud=baud_rate)

# Sistemi tanıyın (heartbeat mesajı bekleyin)
master.wait_heartbeat()
print("Heartbeat received from system (system ID: %d component ID: %d)" % (master.target_system, master.target_component))

# Araç parametreleri
L = 0.6  # Tekerlekler arası mesafe (m)
r = 0.085  # Tekerlek yarıçapı (m)

# Motor hızlarını ayarlayan fonksiyon
def set_motor_speed(left_speed_pwm, right_speed_pwm):
    # PWM değerlerini 1000-2000 aralığına ölçekleyin (örneğin, 0-255 yerine)
    left_speed_pwm = min(max(left_speed_pwm, 1000), 2000)
    right_speed_pwm = min(max(right_speed_pwm, 1000), 2000)
    
    # Sol motor hızı ayarla - pin 1
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,
        1,  # Sol dc motor numarası - pin 1
        left_speed_pwm,  # Sol dc motor PWM (1000-2000)
        0, 0, 0, 0, 0, 0
    )

    # Sağ motor hızı ayarla - pin 2
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,
        2,  # Sağ dc motor numarası - pin 2
        right_speed_pwm,  # Sağ dc motor PWM (1000-2000)
        0, 0, 0, 0, 0, 0
    )

# Motor hızlarını hesaplayan fonksiyon
def calculate_wheel_speeds_pwm(v, w):
    v_r = (2*v+w*L)/(2*r)
    v_l= (2*v-w*L)/(2*r)

    # Hızları PWM değerlerine dönüştürün (örneğin, 1000-2000 arası)
    left_speed_pwm = int(v_l * 1000 / 12.44 + 1000)  # Ölçekleme faktörü uygulayın 
    right_speed_pwm = int(v_r * 1000 / 12.44 + 1000)  # Ölçekleme faktörü uygulayın 

    return left_speed_pwm, right_speed_pwm
