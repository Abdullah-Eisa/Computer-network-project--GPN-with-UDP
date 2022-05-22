from socket import *
from threading import Thread
from time import sleep
from time import time
import matplotlib.pyplot as plt
import sys

clientsocket = socket(AF_INET, SOCK_DGRAM)
print("Started Client UDP File Transfer!")
clientsocket.bind((gethostbyname(gethostname()),0))
print(f"Your host ip and port is {clientsocket.getsockname()}")
max_seg_size = 10000
total_bytes = 0
timestamp = []
ids = []
for i in range(3):
    clientsocket.sendto(sys.argv[1].encode(),(sys.argv[2],int(sys.argv[3])))
    print(f"Waiting for responce from the server (Trial #{i+1})...")
    try:
        start = time()
        received, address = clientsocket.recvfrom(max_seg_size)
        if received:
            packid = -1
            file = open('output.jpg', "wb")
            clientsocket.settimeout(3)
            while True:
                if received[:2] == (packid+1).to_bytes(2, 'big'):
                    file.write(received[2:-1])
                    packid += 1
                    total_bytes += len(received[2:-1])
                    timestamp.append(time()-start)
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
            end = time()
            # change format
            elapsed = end- start
            print(f"Start time: {round(start,2)} seconds, End time: {round(end,2)} seconds")
            
            speed = int((packid+1)/(end-start))
            print(f"The file took on average: {speed} packets/sec, {round(elapsed,2)} seconds")
            print(f"Total number of packets: {packid+1}, total number of bytes: {total_bytes}")
            timestamp = [x*1000 for x in timestamp]
            plt.plot(timestamp, ids)
            plt.xlabel('Time in milliseconds')
            plt.ylabel('Pkt id')
            plt.title('Transmission Graph')
            plt.show()

            file.close()
            break
    except ConnectionResetError: pass
    sleep(2.4)
else: 
    print("Server connection failed after 3 trials")
