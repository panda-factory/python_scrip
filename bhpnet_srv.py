#!/usr/bin/python

import sys
import socket
import getopt
import threading
import subprocess

def usage():
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py ip port"
    print
    print "Examples: "
    print "bhpnet.py 192.168.0.1 5555"
    sys.exit(0)

def main():
    if len(sys.argv[1:]) != 2:
        usage()

    ip_addr = sys.argv[1]
    port = int(sys.argv[2])
    
    server_loop(ip_addr, port)

    return

def server_loop(ip_addr, port):
    if not len(ip_addr):
        ip_addr = "0.0.0.0"

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((ip_addr, port))

    srv.listen(5)
    print "[*] Listening on %s: %d" % (ip_addr, port)

    while True:
        cli_sk, cli_addr = srv.accept()
        print "[*] Client connected from %s: %d" % (cli_addr[0], int(cli_addr[1]))

        cli_thread = threading.Thread(target = client_handler, args = (cli_sk, ))
        cli_thread.start()


def run_command(cmd_buf):
    cmd_buf = cmd_buf.rstrip()

    try:
        output = subprocess.check_output(cmd_buf, stderr = subprocess.STDOUT, shell = True)

    except:
        output = "Failed to execute command.\r\n"

    return output

def client_handler(cli_sk):
    try:
        while True:
            cli_sk.send("<BHP:#> ")
            cmd_buf = ""
            while "\n" not in cmd_buf:
                cmd_buf += cli_sk.recv(1024)
                if not len(cmd_buf):
                    break
 
            response = run_command(cmd_buf)
            cli_sk.send(response)
    except Exception, e:
        print "[!] Threading exit. %s" % e

main()


