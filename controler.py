# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import serial
import time
import zmq,pickle


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

time.sleep(2)

last_t_sent=0
leftTrackVel = 0.
rightTrackVel = 0.
while 1:
    while ser.in_waiting:
        print('driver out = ',ord(ser.read()))

    if len(zmq.select([socket],[],[],0)[0])>0:
        cmd,data = pickle.loads(socket.recv())
        if cmd=='go':
            leftTrackVel,rightTrackVel=data


    if time.time()-last_t_sent>0.1: #10hz
        left_value = int(round(191 + leftTrackVel*63))
        ser.write(b'%c'%left_value)
        right_value = int(round(63 + rightTrackVel*63))
        ser.write(b'%c'%right_value)
        print("sent: {:3} {:3}".format(left_value,right_value ),end='\r')
        last_t_sent=time.time()
        


