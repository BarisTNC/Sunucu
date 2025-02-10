from flask import Flask, request
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Bağlı istemcileri takip etmek için liste
connected_clients = []


def send_server_messages():
    """Server'dan mesaj gönderme fonksiyonu"""
    while True:
        try:
            if connected_clients:
                message = input("\nServer mesajı: ")
                if message.lower() == 'q':
                    break
                socketio.emit('server_message', f'SERVER: {message}')
        except Exception as e:
            print(f"Mesaj gönderme hatası: {e}")
        time.sleep(0.1)


@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    connected_clients.append(client_id)
    print(f'\nYeni istemci bağlandı. ID: {client_id}')
    print(f'Toplam bağlı istemci: {len(connected_clients)}')
    socketio.emit('server_message', 'Sunucuya bağlantı başarılı!')


@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in connected_clients:
        connected_clients.remove(client_id)
    print(f'\nİstemci ayrıldı. ID: {client_id}')
    print(f'Toplam bağlı istemci: {len(connected_clients)}')


@socketio.on('client_message')
def handle_message(message):
    client_id = request.sid
    print(f'\nİstemciden mesaj ({client_id}): {message}')
    # Mesajı diğer tüm istemcilere ilet
    socketio.emit('message_broadcast', f'İstemci {client_id}: {message}', skip_sid=client_id)
    # Mesajı gönderen istemciye onay gönder
    socketio.emit('server_response', f'Mesajınız iletildi', room=client_id)


if __name__ == '__main__':
    print("Server başlatılıyor...")
    # Server mesaj gönderme thread'ini başlat
    message_thread = threading.Thread(target=send_server_messages)
    message_thread.daemon = True
    message_thread.start()

    # Server'ı başlat
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)