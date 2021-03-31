#! /usr/bin/env python3
# Echo server program

import frame
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from threading import Thread

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "server"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets
threadNum = 0

class Threading(Thread):
    def __init__(self, conn, addr):
        global threadNum
        Thread.__init__(self, name="Thread #%d" % threadNum)
        threadNum +=1
        self.conn = conn
        self.addr = addr
    def run(self):
        command = frame.receiveMsg(self.conn)  # Send is the command now, can eventually be recv
        print('Connected by', self.addr)
        filename = frame.receiveMsg(self.conn)
        if os.path.isfile("./serverFiles/"+filename):
            frame.sendMsg(self.conn, b"STOP")
        else:
            frame.sendMsg(self.conn, b"GO")
            try:
                fd = os.open("./serverFiles/"+filename, os.O_CREAT | os.O_WRONLY)
                os.write(fd, frame.receiveMsg(self.conn).encode())
                os.close(fd)
                frame.sendMsg(self.conn, b"File created in server folder.\n")
            except:
                frame.sendMsg(self.conn, b"Error writing file\n")
        self.conn.close()


while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    Threading(conn,addr).start()


