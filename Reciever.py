from socket import *
from threading import Thread
from time import time
from time import ctime
from os import path
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
max_seg_size = 65536 # set it to most maximum
file = [None] * 65536
while True:
    total_bytes = 0
    total_packets = 0
    timestamp = []
    ids = []
    last_pack = -1
    clientsocket.settimeout(1)
    try:
        received, address = clientsocket.recvfrom(max_seg_size)
    except timeout:
        continue
    clientsocket.settimeout(3)
    file = None
    start = time()
    startdate = ctime()
    while True:
        if randint(0,100)<10:
            print("Packet is received and assumed as lost!")
        else:
            total_bytes += len(received)
            total_packets += 1
            packid = int.from_bytes(received[:2], 'big')
            fileid = int.from_bytes(received[2:4], 'big')
            if packid == last_pack+1: 
                last_pack += 1
                print(f"Received packet in order (Packet ID {packid}) (File ID {fileid})") 
                if packid == 0:
                    filename = received[4:-4].decode()
                    if path.exists(filename):
                        c = 2
                        while path.exists(filename+" "+str(c)):
                            c += 1
                        filename += " "+str(c)
                    file = open(filename, "wb")
                else: 
                    file.write(received[4:-4])
                ids.append(packid)
                timestamp.append(time())
                if received[-4:] == b'\xff\xff\xff\xff':
                    print(f"Receiver UDP File Transfer (File ID {fileid}) has successfully finished!")
                    clientsocket.sendto(received[:4],address) # reached or not, i will finish!
                    file.close()
                    break
            else: print(f"Received packet out of order (Packet ID {packid}) (File ID {fileid})")
        if last_pack>=0: clientsocket.sendto((last_pack).to_bytes(2,'big')+received[2:4],address)
        try: received, address = clientsocket.recvfrom(max_seg_size)
        except timeout:
            print("Server connection is lost (timeout)")
            file.close()
            break
    end = time()
    enddate = ctime()
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
