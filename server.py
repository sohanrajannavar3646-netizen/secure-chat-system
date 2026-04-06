import socket
import threading
import ssl

HOST = '127.0.0.1'
PORT = 6000

clients = {}
rooms = {}

def broadcast(message, room, sender):
    for username, client in clients.items():
        if username != sender and rooms.get(username) == room:
            client.send(message.encode())

def handle_client(client, username):
    while True:
        try:
            message = client.recv(1024).decode()

            if message == "/quit":
                room = rooms.get(username, "default")
                print(f"{username} left {room}")

                if username in clients:
                    del clients[username]
                if username in rooms:
                    del rooms[username]

                client.close()
                break

            elif message.startswith("/join"):
                room = message.split()[1]
                rooms[username] = room
                print(f"{username} joined {room}")
                client.send(f"Joined {room}".encode())

            elif message.startswith("/msg"):
                parts = message.split(" ", 2)
                target = parts[1]
                private_msg = parts[2]

                if target in clients:
                    print(f"Private message from {username} to {target}")
                    clients[target].send(f"[Private] {username}: {private_msg}".encode())
                else:
                    client.send("User not found".encode())

            elif message.startswith("/file"):
                parts = message.split(" ", 1)
                filename = parts[1]

                file_data = client.recv(4096)

                room = rooms.get(username, "default")
                print(f"{username} sent file {filename}")

                for user, c in clients.items():
                    if user != username and rooms.get(user) == room:
                        c.send(f"[File] {username} {filename}".encode())
                        c.send(file_data)

            elif message.startswith("/") and not (
                message.startswith("/join") or
                message.startswith("/msg") or
                message.startswith("/file")
            ):
                client.send("Invalid command".encode())

            else:
                room = rooms.get(username, "default")
                broadcast(f"{username}: {message}", room, username)

        except:
            if username in clients:
                del clients[username]
            if username in rooms:
                del rooms[username]
            client.close()
            break

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

server = context.wrap_socket(server, server_side=True)

print("Secure Server started...")

while True:
    client, addr = server.accept()

    username = client.recv(1024).decode()
    clients[username] = client
    rooms[username] = "default"

    print(f"{username} connected securely")

    thread = threading.Thread(target=handle_client, args=(client, username))
    thread.start()