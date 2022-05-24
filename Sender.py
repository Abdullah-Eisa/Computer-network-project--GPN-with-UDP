from socket import *
from os import path
from math import ceil
from collections import deque
from threading import Thread
import sys
serversocket = socket(AF_INET, SOCK_DGRAM)
print("Started Sender UDP File Transfer!")
serversocket.bind((gethostbyname(gethostname()),0))
print(f"Your host ip and port is {serversocket.getsockname()}")
address = (sys.argv[2],int(sys.argv[3]))
filename = sys.argv[1]
win_size = 4
max_seg_size = 1024
timeout_val = 0.05
while True:
    print(f"Next file \"{filename}\" to address {address}")
    if path.exists(filename):
        file = open(filename, "rb")
        file_size = path.getsize(filename)
        num_chunks = ceil(file_size/(max_seg_size-4))
        window = deque()
        chunks_read = 0
        base = 0
        num_retrans = 0
        window.append(filename.encode())
        for i in range(min(num_chunks,win_size-1)):
            window.append(file.read(max_seg_size-4))
            chunks_read += 1
        serversocket.settimeout(timeout_val)
        for i in range(len(window)):
            serversocket.sendto((i).to_bytes(2,'big')+window[i]+b'\x00\x00', address)  
        while True:
            try:
                message, address = serversocket.recvfrom(2)
                ack_num = int.from_bytes(message[:2],'big')
                if ack_num == num_chunks:
                    serversocket.sendto((num_chunks+1).to_bytes(2,'big')+b'\xff\xff', address)
                    file.close()
                    break
                for i in range(min(ack_num-base+1,num_chunks-chunks_read)):
                    window.popleft()
                    window.append(file.read(max_seg_size-4))
                    chunks_read += 1
                    base = min(ack_num,num_chunks-win_size)+1
                    serversocket.sendto((len(window)-1+base).to_bytes(2,'big')+window[-1]+b'\x00\x00', address)
            except timeout: 
                for i in range(len(window)):
                    serversocket.sendto((i+base).to_bytes(2,'big')+window[i]+b'\x00\x00', address)
                num_retrans += 1
        print(f"Number of retransmittions: {num_retrans}")  
    else: print("Error: file does not exist")
    txt = input().split(" ")
    txt.reverse()
    filename = txt.pop()
    address = (txt.pop(), int(txt.pop()))
