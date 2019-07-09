from picamera.array import PiRGBArray
from picamera import PiCamera
import socket
import time
import cv2

HOST=('192.168.1.104',10000)
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(HOST)
server.listen(5)
print "waiting"
connect,addr=server.accept()
print "{} connected".format(addr)
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.hflip = False
camera.vflip = False
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    # show the frame
    ret,imgencode=cv2.imencode('.jpg',image,[cv2.IMWRITE_JPEG_QUALITY,50])
    connect.sendall(imgencode)
    rawCapture.truncate(0)
    if cv2.waitKey(1)==27:
            break
S.close()