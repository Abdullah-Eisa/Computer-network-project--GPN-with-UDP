from socket import *
from threading import Thread
from time import time
from time import ctime
from os import path
from os import rename
from random import randint
import matplotlib.pyplot as plt
def DrawPlots(x,y):
    plt.plot(timestamp, ids)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Packet ID")
    plt.title("Transmission Graph")
    plt.show()
clientsocket = socket(AF_INET, SOCK_DGRAM)
print("Started Receiver UDP File Transfer!")
clientsocket.bind((gethostbyname(gethostname()),0))
print(f"Your host ip and port is {clientsocket.getsockname()}")
max_seg_size = 1024
while True:
    total_bytes = 0
    total_packets = 0
    timestamp = []
    ids = []
    packid = -1
    oldfilename = "OutputFile"+str(randint(0,65536))
    newfilename = ""
    clientsocket.settimeout(1)
    try:
        received, address = clientsocket.recvfrom(max_seg_size)
    except timeout:
        continue
    clientsocket.settimeout(3)
    file = open(oldfilename, "wb")
    start = time()
    startdate = ctime()
    while True:
        if randint(0,100)<10:
            print("Packet is received and assumed as lost!")
        else:
            total_bytes += len(received)
            total_packets += 1
            if received[:2] == (packid+1).to_bytes(2, 'big'): 
                packid += 1
                print(f"Received packet in order (ID {packid})") 
                if received[-2:] == b'\xff\xff':
                    print("Client UDP File Transfer has successfully finished!")
                    break
                if packid == 0:
                    newfilename = received[2:-2].decode()
                else: 
                    file.write(received[2:-2])
                ids.append(packid)
                timestamp.append(time())
            else: print(f"Received packet out of order (ID {int.from_bytes(received[:2],'big')})")
        if packid>=0: clientsocket.sendto((packid).to_bytes(2,'big'),address)
        try: received, address = clientsocket.recvfrom(max_seg_size)
        except timeout:
            print("Server connection is lost (timeout)")
            break
    end = time()
    enddate = ctime()
    file.close()
    if path.exists(newfilename):
        c = 2
        while path.exists(newfilename+" ("+str(c)+")"):
            c += 1
        newfilename += " ("+str(c)+")"
    rename(oldfilename,newfilename)
    print(f"Start time: {startdate}")
    print(f"End time: {enddate}")
    print(f"Time elapsed: {end-start:.2f} seconds")
    if end-start == 0: end += 0.000001
    byte_per_sec = (total_bytes)/(end-start)
    pack_per_sec = (total_packets)/(end-start)
    print(f"The whole transmission took on average: {pack_per_sec:.0f} packets/sec ({byte_per_sec:.0f} bytes/sec)")
    print(f"Total number of all received packets: {total_packets} packets ({total_bytes} bytes)")
    timestamp = [i-start for i in timestamp]
    plotthread = Thread(target=DrawPlots, args=[timestamp, ids])
    plotthread.start()
