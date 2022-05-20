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
MSS = 200


f = open("image.png", "wb")



print('Recieving')
while True:
    data, addr = sock.recvfrom(MSS) # buffer size is 1024 bytes
    print("received message: %s" % data)
    f.write(data)

    if not(data):# if file ended
      break

f.close()

print(f'File size is : {os.path.getsize(f)}')