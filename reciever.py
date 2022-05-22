from socket import *
from threading import Thread
from time import sleep
import sys

clientsocket = socket(AF_INET, SOCK_DGRAM)
print("Started Client UDP File Transfer!")
clientsocket.bind((gethostbyname(gethostname()),0))
print(f"Your host ip and port is {clientsocket.getsockname()}")
for i in range(3):
    clientsocket.sendto(sys.argv[1].encode(),(sys.argv[2],int(sys.argv[3])))
    print(f"Waiting for responce from the server (Trial #{i+1})...")
    try:
        received, address = clientsocket.recvfrom(1024)
        if received:
            packid = -1
            file = open(sys.argv[1], "wb")
            clientsocket.settimeout(1)
            while True:
                if received[:2] == (packid+1).to_bytes(2, 'big'):
                    file.write(received[2:-1])
                    packid += 1
                    print(f"Received packet in order (ID {packid})") 
                else: print(f"Received packet out of order (ID {int.from_bytes(received[:2],'big')})")
                if packid>-1: clientsocket.sendto((packid).to_bytes(2,'big'),address)
                if received[-1:] == b'\xff':
                    print("Client UDP File Transfer has successfully finished!")
                    break
                try: received, address = clientsocket.recvfrom(1024)
                except timeout:
                    print("Server connection is lost (timeout)")
                    file.close()
                    exit()
            file.close()
            break
    except ConnectionResetError: pass
    sleep(2.4)
else: 
    print("Server connection failed after 3 trials")
