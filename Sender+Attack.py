from socket import *
from os import path
from math import ceil
from collections import deque
from threading import Thread
import sys

def simulated_attack():
    '''
    no trailer
    if id exceeds 2^ 16 , reset it

    '''
    serversocket = socket(AF_INET, SOCK_DGRAM)
    print("Started Sender UDP File Transfer!")
    serversocket.bind((gethostbyname(gethostname()),0))
    print(f"Your host ip and port is {serversocket.getsockname()}")
    win_size = 4
    max_seg_size = 1024
    timeout_val = 0.05
    fileid = [None] * 65536
    if len(sys.argv)>1:
        address = (sys.argv[2],int(sys.argv[3]))
        filename = sys.argv[1]
    else:
        txt = input().split(" ")
        txt.reverse()
        filename = txt.pop()
        address = (txt.pop(), int(txt.pop()))
    while True:
        if None in fileid and path.exists(filename):
            nextid = fileid.index(None)
            fileid[nextid] = {}
            f_arr = fileid[nextid]
            f_arr['address'] = address
            f_arr['file'] = open(filename, "rb")
            f_arr['file_size'] = path.getsize(filename)
            f_arr['num_chunks'] = ceil(f_arr['file_size']/(max_seg_size-8))
            f_arr['window'] = deque()
            f_arr['chunks_read'] = 0
            f_arr['base'] = 0
            f_arr['num_retrans'] = 0
            segment = b'\x00\x00'+(nextid).to_bytes(2, 'big')
            segment += filename.encode()+b'\x00\x00\x00\x00'
            f_arr['window'].append(segment)
            for i in [i+1 for i in range(min(f_arr['num_chunks'],win_size-1))]:
                segment = (i).to_bytes(2,'big')
                segment += (nextid).to_bytes(2, 'big')
                segment += f_arr['file'].read(max_seg_size-8)
                f_arr['chunks_read'] += 1
                if f_arr['chunks_read'] == f_arr['num_chunks']:
                    endbit = b'\x00\x00\x00\x00'
                else:
                    endbit = b'\x00\x00\x00\x00'
                segment += endbit
                f_arr['window'].append(segment)
            serversocket.settimeout(timeout_val)
            for i in range(len(f_arr['window'])):
                serversocket.sendto(f_arr['window'][i], address)
            print(f"Started transmissing file \"{filename}\" (ID {nextid}) to address {address}")  
            retries = 0
            while True:
                try:
                    message, address = serversocket.recvfrom(65536)#4)
                    ack_num = int.from_bytes(message[:2],'big')
                    if ack_num not in [(i+f_arr['base'])%65536 for i in range(len(f_arr['window']))]: continue
                    print(f"Received acknowledgement (ACK ID {ack_num}) (File ID {nextid})") 
                    if f_arr['chunks_read'] == f_arr['num_chunks'] and f_arr['num_chunks']%65536 == ack_num:
                        f_arr['chunks_read'] = 0
                        f_arr['file'].seek(0,0)
                        '''f_arr['file'].close()
                        print(f"File transmission (ID {nextid}) has stopped (Number of retransmissions: {f_arr['num_retrans']})")
                        fileid[nextid] = None
                        break'''
                    '''if ack_num == fileid[nextid]['num_chunks']:
                        #fileid[nextid]['chunks_read']=fileid[nextid]['chunks_read'] % fileid[nextid]['num_chunks']
                        fileid[nextid]['chunks_read']=0
                        #fileid[nextid]['file'].close()
                        #break'''
                    min1 = (ack_num-f_arr['base'])%65536+1
                    min2 = f_arr['num_chunks']-f_arr['chunks_read']
                    for i in [(i+f_arr['base']+win_size)%65536 for i in range(min(min1,min2))]:
                        segment = (i).to_bytes(2,'big')
                        segment += (nextid).to_bytes(2, 'big')
                        segment += f_arr['file'].read(max_seg_size-8)
                        f_arr['chunks_read'] += 1
                        if f_arr['num_chunks'] == f_arr['chunks_read']:
                            endbit = b'\x00\x00\x00\x00'
                        else:
                            endbit = b'\x00\x00\x00\x00'
                        segment += endbit
                        f_arr['window'].popleft()
                        f_arr['window'].append(segment)
                        retries = 0
                        serversocket.sendto(f_arr['window'][-1], address)
                    f_arr['base'] = (ack_num+1)%65536
                except timeout:
                    '''if retries == 10: 
                        f_arr['file'].close()
                        print(f"File transmission (ID {nextid}) has stopped (Number of retransmissions: {f_arr['num_retrans']})")
                        fileid[nextid] = None
                        break # if no ack received after 10 retransmissions, sender finishes and closes file '''
                    retries += 1
                    for i in range(len(f_arr['window'])):
                        serversocket.sendto(f_arr['window'][i], address)
                    f_arr['num_retrans'] += 1
        else: print("Error: cannot read file (sending capacity full or file not found)")
        txt = input().split(" ")
        txt.reverse()
        filename = txt.pop()
        address = (txt.pop(), int(txt.pop()))


simulated_attack()









def original_sender():

    serversocket = socket(AF_INET, SOCK_DGRAM)
    print("Started Sender UDP File Transfer!")
    serversocket.bind((gethostbyname(gethostname()),0))
    print(f"Your host ip and port is {serversocket.getsockname()}")
    win_size = 4
    max_seg_size = 1024
    timeout_val = 0.05
    fileid = [None] * 65536
    if len(sys.argv)>1:
        address = (sys.argv[2],int(sys.argv[3]))
        filename = sys.argv[1]
    else:
        txt = input().split(" ")
        txt.reverse()
        filename = txt.pop()
        address = (txt.pop(), int(txt.pop()))
    while True:
        if None in fileid and path.exists(filename):
            nextid = fileid.index(None)
            fileid[nextid] = {}
            f_arr = fileid[nextid]
            f_arr['address'] = address
            f_arr['file'] = open(filename, "rb")
            f_arr['file_size'] = path.getsize(filename)
            f_arr['num_chunks'] = ceil(f_arr['file_size']/(max_seg_size-8))
            f_arr['window'] = deque()
            f_arr['chunks_read'] = 0
            f_arr['base'] = 0
            f_arr['num_retrans'] = 0
            segment = b'\x00\x00'+(nextid).to_bytes(2, 'big')
            segment += filename.encode()+b'\x00\x00\x00\x00'
            f_arr['window'].append(segment)
            for i in [i+1 for i in range(min(f_arr['num_chunks'],win_size-1))]:
                segment = (i).to_bytes(2,'big')
                segment += (nextid).to_bytes(2, 'big')
                segment += f_arr['file'].read(max_seg_size-8)
                f_arr['chunks_read'] += 1
                if f_arr['chunks_read'] == f_arr['num_chunks']:
                    endbit = b'\xff\xff\xff\xff'
                else:
                    endbit = b'\x00\x00\x00\x00'
                segment += endbit
                f_arr['window'].append(segment)
            serversocket.settimeout(timeout_val)
            for i in range(len(f_arr['window'])):
                serversocket.sendto(f_arr['window'][i], address)
            print(f"Started transmissing file \"{filename}\" (ID {nextid}) to address {address}")  
            retries = 0
            while True:
                try:
                    message, address = serversocket.recvfrom(65536)#4)
                    ack_num = int.from_bytes(message[:2],'big')
                    if ack_num not in [(i+f_arr['base'])%65536 for i in range(len(f_arr['window']))]: continue
                    print(f"Received acknowledgement (ACK ID {ack_num}) (File ID {nextid})") 
                    if f_arr['chunks_read'] == f_arr['num_chunks'] and f_arr['num_chunks']%65536 == ack_num:
                        f_arr['file'].close()
                        print(f"File transmission (ID {nextid}) has stopped (Number of retransmissions: {f_arr['num_retrans']})")
                        fileid[nextid] = None
                        break
                    min1 = (ack_num-f_arr['base'])%65536+1
                    min2 = f_arr['num_chunks']-f_arr['chunks_read']
                    for i in [(i+f_arr['base']+win_size)%65536 for i in range(min(min1,min2))]:
                        segment = (i).to_bytes(2,'big')
                        segment += (nextid).to_bytes(2, 'big')
                        segment += f_arr['file'].read(max_seg_size-8)
                        f_arr['chunks_read'] += 1
                        if f_arr['num_chunks'] == f_arr['chunks_read']:
                            endbit = b'\xff\xff\xff\xff'
                        else:
                            endbit = b'\x00\x00\x00\x00'
                        segment += endbit
                        f_arr['window'].popleft()
                        f_arr['window'].append(segment)
                        retries = 0
                        serversocket.sendto(f_arr['window'][-1], address)
                    f_arr['base'] = (ack_num+1)%65536
                except timeout:
                    if retries == 10: 
                        f_arr['file'].close()
                        print(f"File transmission (ID {nextid}) has stopped (Number of retransmissions: {f_arr['num_retrans']})")
                        fileid[nextid] = None
                        break # if no ack received after 10 retransmissions, sender finishes and closes file 
                    retries += 1
                    for i in range(len(f_arr['window'])):
                        serversocket.sendto(f_arr['window'][i], address)
                    f_arr['num_retrans'] += 1
        else: print("Error: cannot read file (sending capacity full or file not found)")
        txt = input().split(" ")
        txt.reverse()
        filename = txt.pop()
        address = (txt.pop(), int(txt.pop()))