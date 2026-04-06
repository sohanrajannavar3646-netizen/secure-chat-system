import socket
import threading
import ssl

HOST = '127.0.0.1'
PORT = 6000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = context.wrap_socket(client, server_hostname='localhost')
client.connect((HOST, PORT))

username = input("Enter username: ")
client.send(username.encode())

def receive():
    while True:
        try:
            message = client.recv(1024).decode()

            if message.startswith("[File]"):
                parts = message.split(" ", 2)
                sender = parts[1]
                filename = parts[2]

                data = client.recv(4096)

                with open("received_" + filename, "wb") as f:
                    f.write(data)

                print(f"Received file from {sender}: {filename}")

            else:
                print(message)

        except:
            break

def write():
    while True:
        message = input()

        if message.startswith("/file"):
            filename = message.split(" ", 1)[1]

            try:
                with open(filename, "rb") as f:
                    data = f.read()

                client.send(message.encode())
                client.send(data)

            except:
                print("File not found")

        else:
            client.send(message.encode())

            if message == "/quit":
                client.close()
                break

threading.Thread(target=receive).start()
threading.Thread(target=write).start()