# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import cv2,time,zmq
import numpy as np



############ connecting to landrov ##################
context = zmq.Context()
sensor_socket = context.socket(zmq.SUB)
sensor_socket.connect("tcp://192.168.8.106:5557")
sensor_socket.setsockopt(zmq.SUBSCRIBE,b'depthimage') 
sensor_socket.setsockopt(zmq.SUBSCRIBE,b'rgbimage') 

control_socket = context.socket(zmq.PUB)
control_socket.connect("tcp://192.168.8.106:5556")
print('connected to landrov server')


############      main loop        ##################

start_time = time.time()
while 1:
    k=cv2.waitKey(20)

    if k!=-1:
        if k  == 27 or k == ord('q'):
            break
        if sensor_socket.poll(0.001):
            topic,msg = sensor_socket.recv_multipart()
            if topic == b'rgbimage':
                img = cv2.imdecode(np.fromstring(buf, dtype=np.uint8),cv2.IMREAD_COLOR)
                cv2.imshow('img',img)
            if topic == b'depthimage':
                depth =  cv2.imdecode(np.fromstring(buf, dtype=np.uint8),cv2.IMREAD_GREYSCALE)  
    
    tdiff= time.time()-start_time 

    if tdiff < 1.0:  #first second moving forward
        cmd = (2.0,2.0)
    elif tdiff < 3.0: # turnning
        cmd = (0.2,-0.2)
    elif tdiff < 4.0: 
        cmd = (-0.2,-0.2) # moving backwards 
    else:
        cmd = (0.0,0.0) # stopping
    
    control_socket.send_multipart(['motor',cmd])


