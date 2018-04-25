# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import cv2,time,zmq
import numpy as np


port = "5557"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://192.168.8.106:%s" % port)
print('connected to landrov server')



while 1:
    k=cv2.waitKey(1)

    if k!=-1:
        if k  == 27 or k == ord('q'):
            break
    buf = socket.recv() 
    #import ipdb;ipdb.set_trace() 
    img = cv2.imdecode(np.fromstring(buf, dtype=np.uint8),cv2.IMREAD_COLOR)
    cv2.imshow('img',img)
