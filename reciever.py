from socket import *
# from BadNet5 import *
import pickle
import hashlib
import sys
import os
import math
import time



ip = "192.168.1.8"
PORT = 2022

sock = socket(AF_INET,SOCK_DGRAM)
sock.bind((ip, PORT))


seqnum = 1
MSS = 100


f = open("message.png", "wb")



print('Recieving')
while True:
    data, addr = sock.recvfrom(MSS) 
    #data = pickle.loads(data)
    print("received message: %s" % data)
    f.write(data)

    #if (data.decode()=='END'):# if file ended
     # break

f.close()
print('closed connection')
#print(f'File size is : {os.path.getsize(f)}')