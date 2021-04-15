class FrameSocket:
    def __init__(self, conn):
        self.conn = conn
        self.buff = ""

    def sendMsg(self, message):
        length = str(len(message))
        framedMessage = length.encode() + b":" + message
        while len(framedMessage):
            startNextMsg = self.conn.send(framedMessage)
            framedMessage = framedMessage[startNextMsg:]

            
    def receiveMsg(self):
        if self.buff == "":
            self.buff += self.conn.recv(100).decode()
        msgLen = ""

        for i in range(len(self.buff)):
            if self.buff[i] == ":":
                self.buff = self.buff[i+1:]
                break
            msgLen += self.buff[i]

        if msgLen == "":
            return ""

        msgLen = int(msgLen)
        msg = ""

        while len(msg) < msgLen:
            if len(self.buff) == 0:
                self.buff = self.conn.recv(100).decode()
            msg += self.buff[0]
            self.buff = self.buff[1:]
        return msg
