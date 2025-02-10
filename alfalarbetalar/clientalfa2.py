import socketio
import threading
import time


class ChatClient:
    def __init__(self):
        # SocketIO istemcisini oluştur
        self.sio = socketio.Client()
        self.running = True
        self.setup_handlers()

    def setup_handlers(self):
        @self.sio.event
        def connect():
            print('\nSunucuya bağlandı!')

        @self.sio.event
        def disconnect():
            print('\nSunucudan ayrıldı')
            self.running = False

        @self.sio.on('server_message')
        def on_server_message(data):
            print(f'\n{data}')
            print("Mesajınız: ", end='', flush=True)

        @self.sio.on('server_response')
        def on_response(data):
            print(f'\nSunucu: {data}')
            print("Mesajınız: ", end='', flush=True)

        @self.sio.on('message_broadcast')
        def on_broadcast(data):
            print(f'\n{data}')
            print("Mesajınız: ", end='', flush=True)

    def send_messages(self):
        while self.running:
            try:
                message = input("Mesajınız: ")
                if message.lower() == 'q':
                    self.running = False
                    break
                self.sio.emit('client_message', message)
            except Exception as e:
                print(f"Hata: {e}")
                self.running = False
                break
            time.sleep(0.1)

    def start(self):
        try:
            print("Sunucuya bağlanılıyor...")
            self.sio.connect('http://127.0.0.1:5000')

            # Mesaj gönderme thread'ini başlat
            message_thread = threading.Thread(target=self.send_messages)
            message_thread.daemon = True
            message_thread.start()

            # Ana döngü
            while self.running:
                time.sleep(0.1)

        except Exception as e:
            print(f"Bağlantı hatası: {e}")
        finally:
            if self.sio.connected:
                self.sio.disconnect()
                print("\nBağlantı kapatıldı.")


if __name__ == '__main__':
    client = ChatClient()
    client.start()