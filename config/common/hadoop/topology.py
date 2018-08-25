#! /usr/bin/python
import sys
import socket

for ip in sys.argv[1:]:
    try:
        (hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(ip)
        tmpStrs = ip.split(".")
        print("/{0}.{1}".format(tmpStrs[1], tmpStrs[2]))
    except:
        print("/default-rack")
