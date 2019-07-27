import socket
import time
import json
from XJBXX import RECV,SEND
from para import szX
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
    def stop(self):
        print("stop")
        self.__init__()
    def __jog(self):
        print("jog")
        pass
    def __f(self):      #forward
        print("forward")
        pass
    def __b(self):      #back
        print("back")
        pass
    def __fl(self):     #forward-left
        print("forward-left")
        pass
    def __fr(self):     #forward-right
        print("forward-right")
        pass
    def __bl(self):     #back-left
        print("back-left")
        pass
    def __br(self):     #back-right
        print("back-right")
        pass
    def __zibi(self):   #turn round
        print("zibi")
        pass
    def __remote(self):
        if (self.jogging):
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
        self.perform()
ktt = suibianxiexie()
def process(data):
    global ktt
    #print(data)
    try:
        jdata=json.loads(data)
        ktt.process(jdata)
    except:
        pass
    #ktt.process(jdata)
    #print("x:{},y:{}".format(jdata[0]["x"],jdata[0]["y"]))
while 1:
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('192.168.43.116', 9920))
    server.listen(5)
    print("waiting")
    connect, addr = server.accept()
    print("{} connected".format(addr))
    while 1:
        try:
            header,data=RECV(connect)
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
