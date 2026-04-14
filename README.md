# Multi-Room Secure Chat System with File Transfer

## Objective

This project implements a secure multi-client chat application using low-level TCP socket programming in Python. It supports dynamic room creation, room-based communication, private messaging, file transfer, secure SSL/TLS communication, timestamped messages, and server-side logging.

## Features

* Multi-client concurrent communication using threading
* Dynamic room creation using `/create`
* Multi-room chat support using `/join`
* Private messaging using `/msg`
* File transfer using `/file`
* User listing inside room using `/users`
* Server monitoring using `/status`
* SSL/TLS secure communication using self-signed certificate
* Timestamped messages
* Graceful disconnect using `/quit`
* Chat logging into `chat_log.txt`

## Commands

* `/create room1` → Create a room
* `/join room1` → Join a room
* `/users` → Show users in current room
* `/status` → Show connected users and active rooms
* `/msg username message` → Private message
* `/file filename` → Send file
* `/quit` → Exit safely

## Technologies Used

* Python
* TCP Socket Programming
* SSL/TLS
* Threading

## How to Run

### Start Server

python server.py

### Start Client

python client.py

## SSL Certificate Generation

openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key

## Architecture

The project follows client-server architecture.
The server accepts secure client connections, manages room membership, processes commands, routes private messages, transfers files, and logs activity.

## Testing Performed

* Tested with multiple concurrent clients
* Tested room creation and joining
* Tested private messaging
* Tested file transfer
* Tested invalid command handling
* Tested graceful disconnect
* Tested SSL secure communication

## Files Included

* server.py
* client.py
* server.crt
* server.key
* notes.txt
* chat_log.txt
* README.md
