import serial

# Arduino'ya bağlanmak için bağlantıyı başlat
connection_string = '/dev/ttyACM0'  # Bağlantı noktası
baud_rate = 9600                   # Baud hızı

# Arduino bağlantısını başlat
master = serial.Serial(connection_string, baud_rate)

# Araç parametreleri
L = 0.6  # Tekerlekler arası mesafe (m)
r = 0.085  # Tekerlek yarıçapı (m)

# Motor hızlarını ayarlayan fonksiyon
def set_motors(pwm_value_R, direction_R, pwm_value_L, direction_L):
    if 0 <= pwm_value_R <= 255 and 0 <= pwm_value_L <= 255:
        # Sağ motor ve sol motor için PWM ve yön bilgilerini gönder
        master.write(f"{pwm_value_R} {direction_R} {pwm_value_L} {direction_L}\n".encode())
    else:
        print("PWM değerleri 0-255 aralığında olmalı.") 

# Motor hızlarını hesaplayan fonksiyon
def calculate_wheel_speeds_pwm(v, w):
    # Hızları hesaplayın
    v_r = (2 * v + w * L) / (2 * r)
    v_l = (2 * v - w * L) / (2 * r)

    # Yönleri belirleyin
    if v_r > 0 :
        direction_R = 1 
    elif v_r < 0 :
        direction_R = 0
    else:
        direction_R =  2
        
        
    # Yönleri belirleyin
    if v_l > 0 :
        direction_L = 1 
    elif v_l < 0 :
        direction_L = 0
    else:
        direction_L =  2
        

    # PWM değerlerine dönüştürme (ölçekleme faktörü)
    pwm_value_R = int(constrain(abs(v_r) * 255 / (r * 2) + 127.5, 0, 255))  # 0-255 aralığında PWM değeri
    pwm_value_L = int(constrain(abs(v_l) * 255 / (r * 2) + 127.5, 0, 255))  # 0-255 aralığında PWM değeri

    return pwm_value_R, direction_R, pwm_value_L, direction_L

# PWM değerini sınırla
def constrain(value, min_value, max_value):
    return max(min_value, min(value, max_value))

# Test örneği
v = 1.0  # İleri hız (m/s)
w = 0.5  # Dönüş hızı (rad/s)

# Motor hızlarını hesapla
pwm_value_R, direction_R, pwm_value_L, direction_L = calculate_wheel_speeds_pwm(v, w)

# Motorları ayarla
set_motors(pwm_value_R, direction_R, pwm_value_L, direction_L)

# Bağlantıyı kapat
master.close()
