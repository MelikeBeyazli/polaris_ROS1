#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 00:16:37 2024

@author: mb
"""

import socket
import json
import rospy
from ultrasonik_bilgi import engel_tespit

HOST = "192.168.1.10"  # The server (Bilgisayar)'s hostname or IP address
PORT = 65432  # The port used by the server

def send_data(client_socket, engel, msg):
    try:
        # Veriyi JSON formatında gönder
        data_to_send = json.dumps({'engel': engel, 'msg': msg})
        client_socket.send(data_to_send.encode())
    except socket.error as e:
        rospy.logerr(f"Veri gönderme hatası: {e}")

def receive_data(client_socket):
    try:
        client_socket.settimeout(5)  # 5 saniye timeout
        data = client_socket.recv(1024).decode()
        return data
    except socket.timeout:
        rospy.logwarn("Sunucudan cevap alınamadı, zaman aşımı.")
        return None
    except socket.error as e:
        rospy.logerr(f"Sunucudan veri alma hatası: {e}")
        return None

if __name__ == "__main__":
    rospy.init_node('main_node')
    rate = rospy.Rate(10)  # 10 Hz

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  # Socket oluştur
        try:
            client_socket.connect((HOST, PORT))
            while not rospy.is_shutdown():
                # Ultrasonik sensör verisini al
                engel, msg = engel_tespit()
                
                # Mesajı gönder
                send_data(client_socket, engel, msg)

                # Sunucudan cevap al
                data = receive_data(client_socket)
                if data:
                    rospy.loginfo(f"Sunucudan gelen cevap: {data}")
                rospy.loginfo(f"Gönderilen mesaj: {msg}")

                # Bekle
                rate.sleep()

        except rospy.ROSInterruptException:
            rospy.loginfo("ROS düğümü kesildi.")
        except socket.error as e:
            rospy.logerr(f"Socket hatası: {e}")
        finally:
            client_socket.close()
