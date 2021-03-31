def sendMsg(s, message):
    length = str(len(message))
    framedMessage = length.encode() + b":" + message
    while len(framedMessage):
        startNextMsg = s.send(framedMessage)
        framedMessage = framedMessage[startNextMsg:]

mbuf = ""

def receiveMsg(s):
    global mbuf
    if mbuf == "":
        mbuf += s.recv(100).decode()
    msgLen = ""

    for i in range(len(mbuf)):
        if mbuf[i] == ":":
            mbuf = mbuf[i+1:]
            break
        msgLen += mbuf[i]

    if msgLen == "":
        return ""

    msgLen = int(msgLen)

    msg = ""

    while len(msg) < msgLen:
        if len(mbuf) == 0:
            mbuf = s.recv(100).decode()
        msg += mbuf[0]
        mbuf = mbuf[1:]
    return msg
