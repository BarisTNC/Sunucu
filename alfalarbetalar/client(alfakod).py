import requests

def start_client(server_url='http://127.0.0.1:5000/message'):
    while True:
        message = input("Enter message to send (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        response = requests.post(server_url, json={"message": message})
        if response.ok:
            print(f"Server response: {response.json()['response']}")
        else:
            print("Failed to send message.")

if __name__ == "__main__":
    start_client()
