#! /usr/bin/env python3
# Echo server program

import framed
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from time import time
from threading import Thread, enumerate
import threading

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

inTransfer = set()
threadNum = 0
transferLock = threading.Lock()


class Threading(Thread):
    def __init__(self, conn, addr):
        global threadNum
        Thread.__init__(self, name="Thread #%d" % threadNum)
        threadNum +=1
        self.conn = conn
        self.addr = addr

    def checkTransfer(self, fileName):
        global inTransfer
        global transferLock
        transferLock.acquire()
        if fileName in inTransfer:
            canTransfer = False
        else:
            canTransfer = True
            inTransfer.add(fileName)
        transferLock.release()
        return canTransfer

    def endTransfer(self, fileName):
        global inTransfer
        inTransfer.remove(fileName)
        
    def run(self):
        frame = framed.FrameSocket(self.conn)
        command = frame.receiveMsg()  # Send is the command now, can eventually be recv
        print('Connected by', self.addr)
        filename = frame.receiveMsg()
        canTransfer = self.checkTransfer(filename)
        
        if os.path.isfile("./serverFiles/"+filename):
            frame.sendMsg(b"STOP")
        else:
            frame.sendMsg(b"GO")
            try:
                fd = os.open("./serverFiles/"+filename, os.O_CREAT | os.O_WRONLY)
                os.write(fd, frame.receiveMsg().encode())
                os.close(fd)
                frame.sendMsg(b"File created in server folder.\n")
            except:
                frame.sendMsg(b"Error writing file\n")
            self.endTransfer(filename)
        self.conn.close()


while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    Threading(conn,addr).start()


