#!/usr/bin/python

import sys
import socket
import getopt
import threading
import subprocess

def usage():
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py ip_addr port"
    print
    print "Examples: "
    print "bhpnet.py 192.168.0.1 5555"
    sys.exit(0)

def main():
    if len(sys.argv[1:]) != 2:
        usage()

    ip_addr = sys.argv[1]
    port = int(sys.argv[2])
    
    cli_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cli_sk.connect((ip_addr, port))
    except:
        print "[!] connect to %s: %d failed." % (ip_addr, potr)

    cli_hander(cli_sk)

    return

def cli_hander(cli_sk):
    try:
        while True:
            recv_len = 1
            response = ""
            while recv_len:
                data = cli_sk.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break;

            print response, 

            buffer = raw_input("")
            buffer += "\n"

            cli_sk.send(buffer)

    except Exception as e :
        print "[*] Exception! Exiting."
        print e
        cli_sk.close()

main()


