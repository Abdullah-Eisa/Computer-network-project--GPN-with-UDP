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
fileid = [None] * 65536
while True:
    if None in fileid and path.exists(filename):
        nextid = fileid.index(None)
        fileid[nextid] = {}
        fileid[nextid]['address'] = address
        fileid[nextid]['file'] = open(filename, "rb")
        fileid[nextid]['file_size'] = path.getsize(filename)
        fileid[nextid]['num_chunks'] = ceil(fileid[nextid]['file_size']/(max_seg_size-4))
        fileid[nextid]['window'] = deque()
        fileid[nextid]['chunks_read'] = 0
        fileid[nextid]['base'] = 0
        fileid[nextid]['num_retrans'] = 0
        segment = b'\x00\x00'+(nextid).to_bytes(2, 'big')
        segment += filename.encode()+b'\x00\x00'
        fileid[nextid]['window'].append(segment)
        for i in range(min(fileid[nextid]['num_chunks'],win_size-1)):
            segment = (fileid[nextid]['chunks_read']+1).to_bytes(2,'big')
            segment += (nextid).to_bytes(2, 'big')
            segment += fileid[nextid]['file'].read(max_seg_size-4)
            if fileid[nextid]['num_chunks']-fileid[nextid]['chunks_read'] == 1:
                endbit = b'\xff\xff'
            else:
                endbit = b'\x00\x00'
            segment += endbit
            fileid[nextid]['window'].append(segment)
            fileid[nextid]['chunks_read'] += 1
        serversocket.settimeout(timeout_val)
        for i in range(len(fileid[nextid]['window'])):
            serversocket.sendto(fileid[nextid]['window'][i], address)
        print(f"Started transmitting file \"{filename}\" (ID {nextid}) to address {address}")  
        retries = 0
        while True:
            try:
                message, address = serversocket.recvfrom(4)
                ack_num = int.from_bytes(message[:2],'big')
                if ack_num == fileid[nextid]['num_chunks']:
                    fileid[nextid]['file'].close()
                    break
                min1 = ack_num-fileid[nextid]['base']+1
                min2 = fileid[nextid]['num_chunks']-fileid[nextid]['chunks_read']
                for i in range(min(min1,min2)):
                    fileid[nextid]['window'].popleft()
                    if fileid[nextid]['chunks_read'] < fileid[nextid]['num_chunks']:
                        segment = (fileid[nextid]['chunks_read']+1).to_bytes(2,'big')
                        segment += (nextid).to_bytes(2, 'big')
                        segment += fileid[nextid]['file'].read(max_seg_size-4)
                        if fileid[nextid]['num_chunks']-fileid[nextid]['chunks_read'] == 1:
                            endbit = b'\xff\xff'
                        else:
                            endbit = b'\x00\x00'
                        segment += endbit
                        fileid[nextid]['window'].append(segment)
                        fileid[nextid]['chunks_read'] += 1
                        serversocket.sendto(fileid[nextid]['window'][-1], address)
                fileid[nextid]['base'] = min(ack_num,fileid[nextid]['num_chunks']-win_size)+1
                retries = 0
            except timeout:
                if retries == 3: break
                retries += 1
                for i in range(len(fileid[nextid]['window'])):
                    serversocket.sendto(fileid[nextid]['window'][i], address)
                fileid[nextid]['num_retrans'] += 1
        print(f"File transmission (ID {nextid}) has stopped!")
        print(f"Number of retransmittions: {fileid[nextid]['num_retrans']}")  
    else: print("Error: cannot read file (sending capacity full or file not found)")
    txt = input().split(" ")
    txt.reverse()
    filename = txt.pop()
    address = (txt.pop(), int(txt.pop()))
