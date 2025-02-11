import socketio
import os
import sys
import pyautogui

class RemoteClient:
    def __init__(self, server_url):
        self.sio = socketio.Client()
        self.server_url = server_url
        self.setup_handlers()

    def setup_handlers(self):
        @self.sio.event
        def connect():
            print('\n[DEBUG] Sunucuya bağlandı!')

        @self.sio.event
        def disconnect():
            print('\n[DEBUG] Sunucudan ayrıldı')
            sys.exit(0)

        @self.sio.on('execute_command')
        def on_execute_command(data):
            command = data.get('command')  # Sunucudan gelen komut
            print(f'\n[DEBUG] Sunucudan komut alındı: {command}')
            self.execute_command(command)  # Komutu çalıştır

    def execute_command(self, command):
        if command == 'mute':
           pyautogui.press("volumemute") # Ses kapatma
        elif command == 'unmute':
            os.system("nircmd.exe mutesysvolume 0")  # Ses açma
        elif command == 'shutdown':
            os.system("shutdown /s /t 1")  # Bilgisayarı kapatma
        else:
            print(f"[ERROR] Geçersiz komut: {command}")

    def start(self):
        try:
            print("[INFO] Sunucuya bağlanılıyor...")
            self.sio.connect(self.server_url)
            print(f"[DEBUG] Bağlantı durumu: {self.sio.connected}")
            self.sio.wait()
        except Exception as e:
            print(f"[ERROR] Bağlantı hatası: {e}")
        finally:
            if self.sio.connected:
                self.sio.disconnect()
                print("\n[INFO] Bağlantı kapatıldı.")

if __name__ == '__main__':
    client = RemoteClient('http://klinkzapp/app/')
    client.start()