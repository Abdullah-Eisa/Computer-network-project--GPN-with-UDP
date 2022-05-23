from socket import *
from threading import Thread
from time import time
from time import ctime
import matplotlib.pyplot as plt
import sys

clientsocket = socket(AF_INET, SOCK_DGRAM)
print("Started Client UDP File Transfer!")
clientsocket.bind((gethostbyname(gethostname()),0))
print(f"Your host ip and port is {clientsocket.getsockname()}")
max_seg_size = 1024
total_bytes = 0
timestamp = []
ids = []
try:
    received, address = clientsocket.recvfrom(max_seg_size)
    if received:
        start = time()
        startdate = ctime()
        packid = -1
        file = open("OutputFile", "wb")
        clientsocket.settimeout(3)
        while True:
            if received[:2] == (packid+1).to_bytes(2, 'big'):
                file.write(received[2:-1])
                packid += 1
                total_bytes += len(received[2:-1])
                timestamp.append(time())
                ids.append(packid)
                print(f"Received packet in order (ID {packid})") 
            else: print(f"Received packet out of order (ID {int.from_bytes(received[:2],'big')})")
            if packid>-1: clientsocket.sendto((packid).to_bytes(2,'big'),address)
            if received[-1:] == b'\xff':
                print("Client UDP File Transfer has successfully finished!")
                break
            try: received, address = clientsocket.recvfrom(max_seg_size)
            except timeout:
                print("Server connection is lost (timeout)")
                break
        file.close()
        end = time()
        enddate = ctime()
        print(f"Start time: {startdate}")
        print(f"End time: {enddate}")
        print(f"Elapsed time: {end-start:.2f} seconds")
        pack_per_sec = (packid+1)/(end-start)
        byte_per_sec = (total_bytes)/(end-start)
        print(f"The file took on average: {pack_per_sec:d} packets/sec ({byte_per_sec:d} bytes/sec)")
        print(f"Total number of packets: {packid+1} packets, total number of bytes: {total_bytes} bytes")
        plt.plot(timestamp, ids)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Packet ID")
        plt.title("Transmission Graph")
        plt.show()
except ConnectionResetError: pass
