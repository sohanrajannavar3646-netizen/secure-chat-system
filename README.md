# Multi-Room Secure Chat System with File Transfer

## Objective

This project implements a secure multi-client chat application using low-level TCP socket programming in Python.
It supports multiple chat rooms, private messaging, secure SSL/TLS communication, and file transfer.

## Features

* Multi-client concurrent communication using threading
* Multi-room chat support
* Private messaging between users
* File transfer within rooms
* SSL/TLS secure communication using self-signed certificate
* Graceful disconnect handling
* Invalid command handling

## Commands

* /join room1 → Join a room
* /msg username message → Private message
* /file filename → Send file
* /quit → Exit safely

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

Clients connect to a threaded secure TCP server.
The server manages room membership, private messaging, and file transfer through command-based protocol.

## Testing Done

* Tested with multiple concurrent clients
* Tested file transfer
* Tested private messaging
* Tested invalid commands
* Tested client disconnect handling
