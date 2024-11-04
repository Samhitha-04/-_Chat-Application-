import socket
import threading
import os

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []
message_history_file = 'chat_history.txt'

# Save message to file
def save_message(message):
    with open(message_history_file, 'a') as file:
        file.write(message + '\n')

# Load previous messages from file
def load_message_history(client):
    if os.path.exists(message_history_file):
        with open(message_history_file, 'r') as file:
            client.send("Previous chat history:\n".encode('utf-8'))
            for line in file:
                client.send(line.encode('utf-8'))

# Broadcast messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))

# Notify online users
def notify_users():
    online_users = "Online users: " + ", ".join(nicknames)
    broadcast(online_users)

# Handle individual client connection
def handle_client(client):
    while True:
        try:
            # Receive and broadcast message
            message = client.recv(1024).decode('utf-8')
            save_message(message)
            broadcast(message)
        except:
            # Handle client disconnect
            index = clients.index(client)
            nickname = nicknames[index]
            clients.remove(client)
            client.close()
            nicknames.remove(nickname)
            broadcast(f'{nickname} has left the chat.')
            save_message(f'{nickname} has left the chat.')
            notify_users()
            break

# Receive new clients
def receive_connections():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        # Request and verify unique nickname
        while True:
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            if nickname in nicknames:
                client.send("Nickname already taken. Choose another.".encode('utf-8'))
            else:
                nicknames.append(nickname)
                clients.append(client)
                break

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} has joined the chat!')
        save_message(f'{nickname} has joined the chat!')
        notify_users()
        client.send('Connected to the server!'.encode('utf-8'))

        # Load message history for new client
        load_message_history(client)

        # Start handling thread for client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is running...")
receive_connections()

