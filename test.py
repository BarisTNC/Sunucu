import requests

# Sunucunun adresi ve portu
server_url = 'http://127.0.0.1:5000/send_command'

# Gönderilecek komut verileri
data = {
    'client_id': '1f71lGluivcTlh2eAAAB',  # Bağlanmak istediğiniz istemcinin ID'si
    'command': 'mute'  # Gönderilecek komut ('mute', 'unmute', 'shutdown', vb.)
}

# POST isteğini gönder
response = requests.post(server_url, json=data)

# Sunucudan gelen yanıtı yazdır
print(response.json())