#!/usr/bin/python

import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))
server.listen(5)

print "[*] Listening on %s: %d" %(bind_ip, bind_port)

def handle_client(cli_sk):
    request = cli_sk.recv(1024)
    print "[*] Received: %s" %request

    cli_sk.send("ACK!")
    cli_sk.close()

while True:
    cli_sk, addr = server.accept()
    print "[*] Accepted connection from: %s: %d" %(addr[0], addr[1])

    cli_handler = threading.Thread(target = handle_client, args = (cli_sk, ))
    cli_handler.start()
