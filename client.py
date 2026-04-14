import socket
import threading
import ssl

HOST = '127.0.0.1'
PORT = 6000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_client = context.wrap_socket(client, server_hostname=HOST)
secure_client.connect((HOST, PORT))

username = input("Enter username: ")
secure_client.send(username.encode())

def receive():
    while True:
        try:
            message = secure_client.recv(1024).decode()
            print(message)
        except:
            break

def write():
    while True:
        message = input()

        if message.startswith("/file"):
            filename = message.split()[1]
            with open(filename, "r") as f:
                data = f.read()
            secure_client.send(f"/file {filename} {data}".encode())

        else:
            secure_client.send(message.encode())

threading.Thread(target=receive).start()
threading.Thread(target=write).start()
