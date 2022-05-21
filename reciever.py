from socket import *
from threading import Thread
import sys

clientsocket = socket(AF_INET, SOCK_DGRAM)
print("Started Client UDP File Transfer!");
for i in range(3):
    clientsocket.sendto(sys.argv[1].encode(),(sys.argv[2],int(sys.argv[3])))
    print("Waiting for responce from the server (Trial #{})...".format(i+1))
    received, address = clientsocket.recvfrom(1024)
    if received:
        curr_packet = -1
        file = open(sys.argv[1], "wb")
        while True:
            if received[:2] == (curr_packet+1).to_bytes(2, 'big'):
                file.write(received[2:-1])
                curr_packet += 1
                print("Received packet in order ID",curr_packet) 
            if curr_packet>-1: clientsocket.sendto((curr_packet).to_bytes(2,'big'),address)
            if received[-1:] == b'\xff':
                print("Client UDP File Transfer has successfully finished!")
                break
            received, address = clientsocket.recvfrom(1024)
        file.close()
        break
else: print("Server connection failed after 3 trials...")
