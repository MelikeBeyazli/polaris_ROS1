# echo-client.py
# Rasğerry pi içerisinde bulunarak bize arayüzde bulunmasını istediğimiz
# verileri aktarmada kullanılacak
import socket
def client():
    HOST = "192.168.250.67"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  # Socket oluştur
        client_socket.connect((HOST, PORT))
        
        message = input("Göndermek istediğiniz mesajı girin: ")
    
        while message.lower().strip() != 'exit':
            # Mesajı gönder
            client_socket.send(message.encode())
            
             # Sunucudan cevap al
            data = client_socket.recv(1024).decode()
            print(f"Sunucudan gelen cevap: {data}")
            
            message = input("Göndermek istediğiniz mesajı girin: ")
    
        client_socket.close()
