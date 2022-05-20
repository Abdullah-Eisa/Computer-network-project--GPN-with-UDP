import socket
import sys
import pickle
import imageio as iio
import os

filename = sys.argv[1]  # file that we want to send

rec_ip = sys.argv[2]  # second argument after file name
rec_port = sys.argv[3] # third argument after ip
MSS = 100  # Maximum Segment size, could be changed


# _________________________________________________

Window_size = 4 # arbitrary number
timeout = 5  # arbitrary number 
base = 1
SeqNum = 1
data_finished = False

#_______________________-

Sender_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # Establish the connection
Sender_socket.settimeout(5)  # arbitrary number
Sender_socket.connect((rec_ip,int(rec_port))) # connect to reciever


# reading the file

f = open(filename, "rb")

data = f.read(MSS)
packets = []
print(f'File size is : {os.path.getsize(filename)}')


while not(data_finished): 
	#data = [str(SeqNum) ,data]
	#data_encoded = [x.encode('utf-8') for x in data]
	#data=pickle.dumps(data)
	Sender_socket.send(data)
	data = f.read(MSS)




	if not(data): # if file ended
		Sender_socket.send('END'.encode())
		data_finished= True







Sender_socket.close()
print("closed Connection")



'''
create socket 

read file

while not done or window :
	if (nextSeqnum < base + window_size):
		read MSS
		send MSS
		neqSeqNum =+ 1

	"recieve ACK"
	Ack = socket_recieve  (int)
	newbase = ack - oldbase (number of steps the window moves)




'''