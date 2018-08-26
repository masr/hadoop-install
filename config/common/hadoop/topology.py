#! /usr/bin/python
import sys
import socket

for ip in sys.argv[1:]:
    try:
        (hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(ip)
        tmpStrs = ip.split(".")
        print("/{0}.{1}.{2}".format(tmpStrs[0], tmpStrs[1], tmpStrs[2]))
    except:
        print("/default-rack")
