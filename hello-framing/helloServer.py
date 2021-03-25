#! /usr/bin/env python3
import frame
# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)
        filename = frame.recieveMsg(conn)
        print("Attemting to clone file from client; filename: " + filename)
        if not os.path.isfile("./server/" + filename):
            fd = os.open("./server/" +filename, os.O_CREAT | os.O_WRONLY)
            os.write(fd, frame.recieveMsg(conn).encode())
            os.close(fd)
            print("File created in server folder.")
        else:
            print("File already exists")
        conn.shutdown(socket.SHUT_WR)


