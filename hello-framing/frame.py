def sendMsg(s, message):
    length = len(message)
    framedMessage = str(length) + ":" + message
    framedMessage = str(framedMessage).encode()
    while len(framedMessage):
        startNextMsg = s.send(framedMessage)
        framedMessage = framedMessage[startNextMsg:]

mbuf = ""

def recieveMsg(s):
    global mbuf
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
        msg += mbuf[0]
        if len(mbuf) == 1:
            mbuf = s.recv(100).decode()
        mbuf = mbuf[1:]
    return msg
