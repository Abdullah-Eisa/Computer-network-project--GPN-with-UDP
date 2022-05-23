from socket import *
from os import path
from math import ceil
from collections import deque
from threading import Thread
import sys

serversocket = socket(AF_INET, SOCK_DGRAM)
print("Started Server UDP File Transfer!")
serversocket.bind((gethostbyname(gethostname()),0))
print(f"Your host ip and port is {serversocket.getsockname()}")
address = (sys.argv[2],int(sys.argv[3]))
win_size = 4
max_seg_size = 1024
timeout_val = 0.05
file = open(sys.argv[1], "rb")
file_size = path.getsize(sys.argv[1])
num_chunks = ceil(file_size/(max_seg_size-3))
window = deque()
chunks_read = 0
base = 0
num_retrans = 0
for i in range(min(num_chunks,win_size)):
    window.append(file.read(max_seg_size-3))
    chunks_read += 1
serversocket.settimeout(timeout_val)
endbit = b'\x00'
for i in range(len(window)):
    if i == num_chunks - 1: endbit = b'\xff'
    serversocket.sendto((i).to_bytes(2,'big')+window[i]+endbit, address)  
while True:
    endbit = b'\x00'
    try:
        message, address = serversocket.recvfrom(2)
        ack_num = int.from_bytes(message[:2],'big')
        if ack_num == num_chunks - 1:
            file.close()
            break
        for i in range(min(ack_num-base+1,num_chunks-chunks_read)):
            window.popleft()
            window.append(file.read(max_seg_size-3))
            chunks_read += 1
            base = min(ack_num+1,num_chunks-win_size)
            if chunks_read == num_chunks: endbit = b'\xff'
            serversocket.sendto((window[win_size-1]).to_bytes(2,'big')+window[-1]+endbit, address)
    except timeout: 
        for i in range(len(window)):
            if i+base == num_chunks - 1: endbit = b'\xff'
            serversocket.sendto((i+base).to_bytes(2,'big')+window[i]+endbit, address)
        num_retrans += 1
print(f"Number of retransmittions: {num_retrans}")  
