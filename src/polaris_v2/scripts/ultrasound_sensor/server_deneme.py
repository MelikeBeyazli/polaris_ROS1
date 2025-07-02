#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 11:00:19 2024

@author: mb
"""

# echo-server.py

import socket

HOST = "192.168.250.67"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:  # Socket oluştur
    server_socket.bind((HOST, PORT))  # Socket bağla
    
    # Sunucuyu dinlemeye başla
    server_socket.listen()
    print("Sunucu başlatıldı. Bağlantı bekleniyor...")
     
    conn, addr = server_socket.accept()
    with conn:
        print(f"Bağlantı alındı: {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                print("Veri gelmedi")
                break
            print(f"İstemciden gelen veri:{data.decode()}")
            # İstemciye cevap gönder
            response = 'Veri alındı: '+ data.decode()
            conn.sendall(data)
        conn.close()
        print("Bağlantı kapatıldı.")
        