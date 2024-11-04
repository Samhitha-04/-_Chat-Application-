import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

nickname = input("Choose a unique nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receive messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break

# Send messages to the server
def send_messages():
    while True:
        message = input("")
        if message:
            if message.lower() == '/quit':
                client.send(f'{nickname} has left the chat.'.encode('utf-8'))
                client.close()
                break
            client.send(f'{nickname}: {message}'.encode('utf-8'))

# Notify typing
def typing_indicator():
    while True:
        message = input("")
        if message:
            if message.lower() == '/quit':
                client.send(f'{nickname} has left the chat.'.encode('utf-8'))
                client.close()
                break
            client.send(f'{nickname}: {message}'.encode('utf-8'))

# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()


