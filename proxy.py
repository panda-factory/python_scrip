#!/usr/bin/python
import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s: %d" % (local_host, local_port)
        print "[!!] Check for other listeningn sockets or correct permissions."
        sys.exit(0)

    print "[*] Listening on %s: %d" % (local_host, local_port)

    server.listen(5)

    while True:
        cli_sk, addr = server.accept()
        print "[=>] Received incoming connection from %s: %d" % (addr[0], addr[1])

        proxy_thread = threading.Thread(target = proxy_handler, args = (cli_sk, remote_host, remote_port))
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 4:
        print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000"
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    server_loop(local_host, local_port, remote_host, remote_port)

def proxy_handler(cli_sk, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    while True:
        local_buffer = receive_from(cli_sk)
        if len(local_buffer):
            print "[=>] Received %d bytes from localhost." % len(local_buffer)
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)

            remote_socket.send(local_buffer)
            print "[=>] Sent to remote."
        
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print "[<=] Received %d bytes from remote." % len(remote_buffer)
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)

            cli_sk.send(remote_buffer)
            print "[<=] Sent to localhost."

def hexdump(src, length = 16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
        s = src[i: i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X %-*s %s" % (i, length*(digits + 1), hexa, text))

    print b'\n'.join(result)

def receive_from(conn):
    buffer = ""

    conn.settimeout(2)

    try:
        while True:
            data = conn.recv(4096)
            print "%s" % data
            if not data:
                break

            buffer += data
    except:
        pass
    return buffer

def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

main()
