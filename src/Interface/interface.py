# -*- coding: utf-8 -*-
# !/usr/bin/env python3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from polaris_ui import Ui_Polaris
import socket
import threading

class PolarisApp(QtWidgets.QMainWindow, Ui_Polaris):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Initially show the intro panel
        self.stackedWidget.setCurrentWidget(self.intro_panel)

        # Use QTimer to transition to start panel after 5 seconds
        QtCore.QTimer.singleShot(5000, self.show_start_panel)

        # Connect StartButton to function
        self.StartButton.clicked.connect(self.start_button_clicked)
        self.manuelButton.clicked.connect(self.manuel_button_clicked)
        self.otonombutton.clicked.connect(self.otonom_button_clicked)

        # Server variables
        self.host = '192.168.1.21'
        self.port = 12346
        self.server_socket = None
        self.client_socket = None
        self.client_address = None

        # Thread lock for updating UI from thread
        self.lock = threading.Lock()

        # Counter for loading bar value
        self.loading_counter = 0

        # Timer for updating the loading bar
        self.loading_timer = QtCore.QTimer(self)
        self.loading_timer.timeout.connect(self.update_loading_bar)

        # Initialize a set to keep track of pressed keys
        self.pressed_keys = set()
    def update_loading_bar(self, message=""):
        """Yükleme çubuğu değerini ve mesajını günceller."""
        if self.loading_counter < 100:
            self.loading_counter += 2
            self.loading_no.setText(f"%{self.loading_counter}")
            self.loading_info.setText(message)
            if self.loading_counter >= 100:
                # Kontrol paneline geçişi başlat
                self.show_control_panel()
                self.loading_timer.stop()
        else:
            self.loading_counter = 100
            self.loading_no.setText(f"%{self.loading_counter}")

    def show_start_panel(self):
        """Intro panelden start paneline geçiş yapar."""
        self.stackedWidget.setCurrentWidget(self.start_panel)

    def show_control_panel(self):
        """Start panelden control paneline geçiş yapar."""
        self.stackedWidget.setCurrentWidget(self.control_panel)

    def start_button_clicked(self):
        """Yeni bir thread'de sunucuyu başlatır."""
        threading.Thread(target=self.run_server).start()

    def manuel_button_clicked(self):
        """Manuel modu aktif eder ve klavye olaylarını işler."""
        self.is_manuel_mode = True
        self.send_command_to_client("START_MANUEL_MODE")
        self.setFocus()  # Bu pencerenin odaklanmasını sağlayarak tuş olaylarını yakalar
    def otonom_button_clicked(self):
        """Manuel modu aktif eder ve klavye olaylarını işler."""
        self.is_manuel_mode = False
        self.send_command_to_client("START_AUTONOMOUS_MODE")
    def run_server(self):
        """Sunucuyu çalıştırır ve bağlantıları yönetir."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Soketi belirtilen IP ve porta bağla
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.update_loading_bar("Sunucu başlatıldı, dinleniyor...")

            while True:
                self.update_loading_bar("İstemci bağlantısı bekleniyor...")
                self.client_socket, self.client_address = self.server_socket.accept()
                self.update_loading_bar(f"İstemci bağlandı: {self.client_address}")
                threading.Thread(target=self.start_panel_handle_client, daemon=True).start()
                break

        except socket.error as e:
            self.update_loading_bar(f"Bağlantı hatası: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
            if self.client_socket:
                self.client_socket.close()

    def start_panel_handle_client(self):
        """Bağlı bir istemci ile iletişimi yönetir."""
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode()
                self.update_loading_bar(f"İstemciden alındı: {message}")
        except socket.error as e:
            self.update_loading_bar(f"İstemci hatası: {e}")

    def send_command_to_client(self, command):
        """Bağlı istemciye komut gönderir."""
        if self.client_socket:
            try:
                self.client_socket.send(command.encode())
            except socket.error as e:
                self.update_loading_bar(f"Komut gönderme hatası: {e}")

    def keyPressEvent(self, event):
        """Manuel kontrol için tuş basma olaylarını işler."""
        if self.is_manuel_mode:
            key = event.key()
            self.pressed_keys.add(key)
            command = ""
            if QtCore.Qt.Key_W in self.pressed_keys:
                command = "FORWARD"
                if QtCore.Qt.Key_Space in self.pressed_keys:
                    command = "FORWARD_FAST"
            elif QtCore.Qt.Key_S in self.pressed_keys:
                command = "BACKWARD"
                if QtCore.Qt.Key_Space in self.pressed_keys:
                    command = "BACKWARD_FAST"
            elif QtCore.Qt.Key_A in self.pressed_keys:
                command = "LEFT"
            elif QtCore.Qt.Key_D in self.pressed_keys:
                command = "RIGHT"

            if command:
                self.send_command_to_client(command)

    def keyReleaseEvent(self, event):
        """Manuel kontrol için tuş bırakma olaylarını işler."""
        key = event.key()
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("logo4.png"))
    window = PolarisApp()
    window.show()
    sys.exit(app.exec_())
