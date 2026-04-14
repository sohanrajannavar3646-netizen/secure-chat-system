import socket
import threading
import ssl
from datetime import datetime

HOST = '127.0.0.1'
PORT = 6000

clients = {}
rooms = {}
available_rooms = {"default"}

def log_message(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")

def timestamp():
    return datetime.now().strftime("[%H:%M:%S]")

def broadcast(message, room, sender):
    for username, client in clients.items():
        if username != sender and rooms.get(username) == room:
            client.send(message.encode())

def handle_client(client, username):
    while True:
        try:
            message = client.recv(1024).decode()

            if message.startswith("/create"):
                room = message.split()[1]
                available_rooms.add(room)
                rooms[username] = room
                client.send(f"Room {room} created and joined".encode())

            elif message.startswith("/join"):
                room = message.split()[1]

                if room in available_rooms:
                    rooms[username] = room
                    client.send(f"Joined {room}".encode())
                else:
                    client.send("Room does not exist".encode())

            elif message.startswith("/users"):
                room = rooms[username]
                user_list = [u for u in rooms if rooms[u] == room]
                client.send(f"Users in {room}: {', '.join(user_list)}".encode())

            elif message.startswith("/status"):
                client.send(f"Connected users: {len(clients)} | Rooms active: {len(available_rooms)}".encode())

            elif message.startswith("/msg"):
                parts = message.split(" ", 2)
                target = parts[1]
                private_msg = parts[2]

                if target in clients:
                    msg = f"{timestamp()} [Private] {username}: {private_msg}"
                    clients[target].send(msg.encode())

            elif message.startswith("/file"):
                parts = message.split(" ", 2)
                filename = parts[1]
                filedata = parts[2]

                room = rooms[username]
                msg = f"{timestamp()} FILE from {username}: {filename} -> {filedata}"

                for user, c in clients.items():
                    if rooms.get(user) == room and user != username:
                        c.send(msg.encode())

                log_message(msg)

            elif message == "/quit":
                client.close()
                del clients[username]
                del rooms[username]
                break

            else:
                room = rooms[username]
                msg = f"{timestamp()} {username}: {message}"
                broadcast(msg, room, username)
                log_message(msg)

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

secure_server = context.wrap_socket(server, server_side=True)

print("Secure server started...")

while True:
    client, addr = secure_server.accept()

    username = client.recv(1024).decode()
    clients[username] = client
    rooms[username] = "default"

    print(f"{username} connected")

    thread = threading.Thread(target=handle_client, args=(client, username))
    thread.start()
