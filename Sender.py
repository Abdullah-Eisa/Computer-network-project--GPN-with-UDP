from socket import *
from os import path
from math import ceil

serversocket = socket(AF_INET, SOCK_DGRAM)
print("Started Server UDP File Transfer!")

serversocket.bind((gethostbyname(gethostname()),0))
print(f"Your host ip and port is {serversocket.getsockname()}")

message, address = serversocket.recvfrom(1024)
file = open(message.decode(), "rb")
file_size = path.getsize(message.decode())
num_chunks = ceil(file_size/1021)
endbit = b'\x00'
for i in range(num_chunks):
    data = file.read(1021)
    if i == num_chunks - 1: endbit = b'\xff'
    while True:
        serversocket.sendto((i).to_bytes(2,'big')+data+endbit, address)
        message, address = serversocket.recvfrom(2)
        if message[:2] == (i).to_bytes(2, 'big'): break
file.close()
