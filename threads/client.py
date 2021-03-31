#! /usr/bin/env python3
import frame

# Echo client program
import os, socket, sys, re, time
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "client"
#paramMap = params.parseParams(switchesVarDefaults)

#server, usage  = paramMap["server"], paramMap["usage"]

#if usage:
#    params.usage()

try:
    clientFile = sys.argv[1]
    serverHost, serverFile = re.split(":", sys.argv[2])
    serverPort = 50001
except:
    print("Unable to correctly read params: '%s'. Please format as: $ ./client Send {client file} {host:serverFile}\n" % sys.argv)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

"""
delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(delay)
    print("done sleeping")
"""
message = ""
frame.sendMsg(s, sys.argv[0].encode())
frame.sendMsg(s, serverFile.encode())
response = frame.receiveMsg(s)
if response == "GO":
    fd = os.open("./clientFiles/" + clientFile, os.O_RDONLY)
    while 1:
        ibuf = os.read(fd,100)
        sbuf = ibuf.decode()
        if len(sbuf) == 0:
            break
        message += sbuf

    frame.sendMsg(s, message.encode())
    result = frame.receiveMsg(s)
    os.write(1, result.encode())
else:
    os.write(1, b"File name alrady exists.\n")


s.close()
