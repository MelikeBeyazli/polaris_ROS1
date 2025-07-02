import serial
import time

# Seri portu ve baud hızını belirleyin
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

def send_data(data):
    arduino.write(bytes(data, 'utf-8')) # Veriyi byte olarak gönder
    time.sleep(0.05)
    return

while True:
    data_to_send = input("Arduino'ya göndermek istediğiniz veriyi girin: ") # Kullanıcıdan veri al
    send_data(data_to_send) # Veriyi Arduino'ya gönder
    
    
"""
void setup() {
  Serial.begin(9600); // Seri iletişimi 9600 baud hızında başlat
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readString(); // Seri porttan gelen veriyi oku
    Serial.println(data); // Gelen veriyi Seri Monitör'e yazdır
  }
}

"""
