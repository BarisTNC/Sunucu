from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Bağlı istemcileri takip etmek için sözlük
connected_clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    print(f'\n[DEBUG] Yeni istemci bağlandı. ID: {client_id}')
    connected_clients[client_id] = {'id': client_id, 'status': 'connected'}
    emit('update_client_list', list(connected_clients.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in connected_clients:
        del connected_clients[client_id]
    print(f'\n[DEBUG] İstemci ayrıldı. ID: {client_id}')
    emit('update_client_list', list(connected_clients.values()), broadcast=True)

@socketio.on('send_command')
def handle_send_command(data):
    client_id = data.get('client_id')  # Hedef istemcinin ID'si
    command = data.get('command')      # Gönderilecek komut
    print(f'\n[DEBUG] İstemciye komut gönderiliyor. ID: {client_id}, Komut: {command}')
    emit('execute_command', {'command': command}, room=client_id)  # Sadece belirli bir istemciye gönder

if __name__ == '__main__':
    print("[INFO] Sunucu başlatılıyor...")
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)