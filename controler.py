# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import serial
import time
import zmq,pickle


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(4)

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind("tcp://*:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE,b'motor') 


last_t_sent=0
leftTrackVel = 0.
rightTrackVel = 0.
while 1:
    while ser.in_waiting:
        print('driver out = ',ord(ser.read()))

    if socket.poll(0.001): 
        topic, msg = socket.recv_multipart() 
        data = pickle.loads(msg)
        if topic==b'motor':
            leftTrackVel,rightTrackVel=data


    if time.time()-last_t_sent>0.1: #10hz
        left_value = int(round(191 + leftTrackVel*63))
        right_value = int(round(63 + rightTrackVel*63))
        #print("sent: {:3} {:3}".format(left_value,right_value ),end='\r')
        print("sent: {:3} {:3} {} {}".format(left_value,right_value,leftTrackVel, rightTrackVel ))
        ser.write(b'%c'%right_value)
        time.sleep(0.01)
        ser.write(b'%c'%left_value)
        last_t_sent=time.time()
        


