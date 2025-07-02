import socket

# Sunucunun IP adresi ve port numarası
host = '10.0.2.15'
port = 12345

# Socket oluşturma
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Soketi belirtilen IP ve port'a bağlama
server_socket.bind((host, port))

# Sunucuyu dinlemeye başlama
server_socket.listen(1)
print(f"Server {port} portunda dinliyor...")

# Bağlantıyı kabul etme
client_socket, client_address = server_socket.accept()
print(f"Bağlanan: {client_address}")

# Gönderilecek veri
data = "Merhaba, bu bir test mesajıdır."
client_socket.send(data.encode())

# Bağlantıyı kapatma
client_socket.close()
server_socket.close()
