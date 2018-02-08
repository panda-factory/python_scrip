#!/usr/bin/python
#-*- coding: utf-8 -*- 
#author: orangleliu date: 2014-11-12 
#python2.7.x ip_scaner.py 
  
import sys 
import os 
import time 
import threading
        
#执行ping -c 1 xxx.xxx.xxx.xxx命令，判断如果存在TTL字段则该IP被使用
def ping_ip(ip_str): 
    cmd = "ping -c 1 %s" %ip_str
    output = os.popen(cmd).readlines()

    flag = False
    for line in list(output): 
        if not line: 
            continue
        if str(line).upper().find("TTL") >=0: 
            flag = True
            break
    if flag: 
        print "ip: %s is using ***" %ip_str 

#使用多线程执行ping命令对1-254的ip进行扫描
def scan_ip(ip_prefix): 
    threads = []
    for i in range(1, 255): 
        ip = "%s.%s" %(ip_prefix, i) 
        thread = threading.Thread(target=ping_ip, args=(ip,))
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
        
                                                                                                                          
if __name__ == "__main__": 
    print "start time %s"%time.ctime() 
    args = sys.argv[1]   
    args = args.split('.')[:-1]
    args = '.'.join(args) 
    scan_ip(args) 
    print "end time %s"%time.ctime()
