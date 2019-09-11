import socket
import time
import struct
import json
from local_driver import motor
# from XJBXX import RECV, SEND, dataBuffer
from para import szX,IPADD
startTime = 0
class suibianxiexie:
    'zhe sha'
    def __init__(self):
        self.mode="remote"
        self.jogging=0
        self.left=0
        self.right=0
        self.up=0
        self.down=0
        self.X=0
        self.Y=0
        self.J=motor(16,20, 21)
        self.L=motor(23, 24, 18)
        self.R=motor(22, 27, 17)
        self.J.start(0)
        self.L.start(0)
        self.R.start(0)
        self.soft=0
    def stop(self):
        #print("stop")
        self.mode = "remote"
        self.jogging = 0
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0
        self.X = 0
        self.Y = 0
        self.soft=0
        self.J.start(0)
        self.L.start(0)
        self.R.start(0)
    def __jog(self):
        if (self.jogging):

            #print("jog")
            if self.soft==1:
                self.J.start(10*self.jogging)
            else:
                self.J.start(100*self.jogging)
            #self.L.start(0)
            #self.R.start(0)
        else:
            self.J.start(0)
            #self.L.start(0)
            #self.R.start(0)
    def __f(self):      #forward
        #print("forward")
        #self.J.start(0)
        self.L.start(100)
        self.R.start(100)
    def __b(self):      #back
        #print("back")
        #self.J.start(0)
        self.L.start(-100)
        self.R.start(-100)
    def __fl(self):     #forward-left
        #print("forward-left")
        #self.J.start(0)
        self.L.start(100)
        self.R.start(0)
    def __fr(self):     #forward-right
        #print("forward-right")
        #self.J.start(0)
        self.L.start(0)
        self.R.start(100)
    def __bl(self):     #back-left
        #print("back-left")
        #self.J.start(0)
        self.L.start(0)
        self.R.start(-100)
    def __br(self):     #back-right
        #print("back-right")
        #self.J.start(0)
        self.L.start(-100)
        self.R.start(0)
    def __zibi(self):   #turn round
        #print("zibi")
        #self.J.start(0)
        self.L.start(100)
        self.R.start(-100)
    def __remote(self):
        self.__jog()
        if(self.up and self.left):
            self.__fl()
        elif (self.up and self.right):
            self.__fr()
        elif (self.up):
            self.__f()
        elif(self.down and self.left):
            self.__bl()
        elif (self.down and self.right):
            self.__br()
        elif (self.down):
            self.__b()
    def __trace(self):
        if(self.X>0):
            if(self.X<szX/2):
                self.__fl()
            else:
                self.__fr()
        else:
            self.__zibi()
    def perform(self):
        if (self.mode=="remote"):
            self.__remote()
        if (self.mode=="trace"):
            self.__trace()
    def process(self,ins):
        self.X,self.Y=ins[0]["x"],ins[0]["y"]
        k=ins[0]["key"]
        if k==ord("w"):
            print("w")
            self.up=1
            self.down=0
            self.left=0
            self.right=0
        elif k==ord("s"):
            print("s")
            self.up=0
            self.down=1
            self.left = 0
            self.right = 0
        elif k==ord("a"):
            print("a")
            self.left=1
            self.right=0
        elif k==ord("d"):
            print("d")
            self.left=0
            self.right=1
        elif k==ord(" "):
            print("Space")
            self.stop()
        elif k==ord("j"):
            print("j")
            self.jogging = 1
        elif k==ord("k"):
            print("k")
            self.jogging = 0
        elif k==ord("t"):
            print("t")
            self.mode = "trace"
        elif k==ord("r"):
            print("r")
            self.mode="remote"
        elif k==ord("l"):
            print("l")
            self.jogging = -1
        elif k==ord("p"):
            self.soft = 1-self.soft
        self.perform()
ktt = suibianxiexie()

dataBuffer=bytes()
headerSize=12
bias = 0

def RECV(conn):
    global dataBuffer
    global headerSize
    #print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if data:
            dataBuffer += data
            while True:
                if len(dataBuffer) < headerSize:
                    break
                headPack = struct.unpack('!3I', dataBuffer[:headerSize])
                bodySize = headPack[1]
                if len(dataBuffer) < headerSize+bodySize:
                    break
                body = dataBuffer[headerSize:headerSize+bodySize]
                dataBuffer = dataBuffer[headerSize + bodySize:]
                jdata = json.loads(body)[0]
                diff = -jdata['time']+time.time()+bias
                print(diff, len(dataBuffer))
                if diff > 0.07:
                    # tmpdata = conn.recv(1)
                    dataBuffer = bytes()
                    print('clear')
                return headPack, body
        else:
            dataBuffer=bytes()
            return 0,dataBuffer

def SEND(client, body):
    ver = 1
    #body = json.dumps(dict(hello="world"))
    #print(body)
    cmd = 101
    header = [ver, body.__len__(), cmd]
    headPack = struct.pack("!3I", *header)
    sendData = headPack + body.encode()
    client.sendall(sendData)


def SENDI(client, body):
    ver = 2
    #body = json.dumps(dict(hello="world"))
    #print(body)
    cmd = 101
    header = [ver, body.__len__(), cmd]
    headPack = struct.pack("!3I", *header)
    client.sendall(headPack)
    client.sendall(body)


def process(data):
    global ktt
    #print(data)
    # try:
    jdata=json.loads(data)
    # print(data, time.time()-jdata[0]['time'])
    ktt.process(jdata)
    # except:
    #     pass
    #ktt.process(jdata)
    #print("x:{},y:{}".format(jdata[0]["x"],jdata[0]["y"]))

while 1:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IPADD, 9920))
    server.listen(5)
    print("waiting")
    connect, addr = server.accept()
    print("{} connected".format(addr))
    header, data = RECV(connect)
    bias = json.loads(data)[0]['time'] - time.time()
    while 1:
        try:
            header, data = RECV(connect)
            #data=connect.recv(65535)
        except:
            connect.sendall("What's your problem?")
            print("connection failed!!!")
            break
        if not data:
            try:
                connect.sendall("What's your problem?")
            except:
                break
        else:
            process(data)
        #print("Received:{}\r".format(data))
    server.close()
    ktt.stop()
GPIO.cleanup()
