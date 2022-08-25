from socket import *
from PIL import Image
import numpy as np
import json
import zipfile
import os


serverName = 'localhost'
serverPort = 12203
f0 = 'Resources/IMG0.JPG'
f1 = 'Resources/IMG1.JPG'
f2 = 'Resources/IMG2.JPG'
f3 = 'Resources/IMG3.JPG'
#f2 = 'Resources/hkss.jpg'

foc = 1091.110204


def sDat(sN, sP, dd):
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((sN, sP))
	if not isinstance(dd, str):
		dd.save('t.png')
		tempp = open('t.png', 'rb')
		l = tempp.read(1024)
		while l:
			clientSocket.send(l)
			l = tempp.read(1024)
		print("File Sent")
		tempp.close()
		os.remove('t.png')
	else:
		tempp = "Clear".encode()
		clientSocket.send(tempp)
		print("Code 01 Sent")
	clientSocket.shutdown(1)
	retMes = clientSocket.recv(1024).decode()
	print(retMes)
	clientSocket.close()


#clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket.connect((serverName, serverPort))
#
#img0 = Image.open(f0)
#img0.save('temp.png')
#tempp = open('temp.png', 'rb')
#print(img0)
#l = tempp.read(1024)
#while l:
#	clientSocket.send(l)
#	l = tempp.read(1024)
#print("File Sent")
#tempp.close()
#os.remove('temp.png')
#clientSocket.shutdown(1)
#retMes = clientSocket.recv(1024).decode()
#print(retMes)
#clientSocket.close()
#
#
#tempp = open(f1, 'rb')
##img1 = np.array(Image.open(f1))
##clientSocket.send(img1.tobytes())
#l = tempp.read(1024)
#clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket.connect((serverName, serverPort))
#while l:
#	clientSocket.send(l)
#	l = tempp.read(1024)
#print("File Sent")
#tempp.close()
##os.remove('temp.png')
#clientSocket.shutdown(1)
#retMes = clientSocket.recv(1024).decode()
#print(retMes)
#clientSocket.close()
#
#
#clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket.connect((serverName, serverPort))
#
#clientSocket.send("Clear".encode())
#clientSocket.close()
#print("Finished")

sDat(serverName, serverPort, Image.open(f2))
sDat(serverName, serverPort, Image.open(f3))
sDat(serverName, serverPort, "Clear")

s = socket(AF_INET, SOCK_STREAM)
s.connect((serverName, 12302))
print("Connected")
l = json.dumps((25.573, 38.131, 13.191))
s.send(l.encode())
retMess = s.recv(1024).decode()
print(retMess)
s.close()

s = socket(AF_INET, SOCK_STREAM)
s.connect((serverName, 12302))
print("Connected")
l = json.dumps((23.622, 44.699, 19.95))
s.send(l.encode())
retMess = s.recv(1024).decode()
print(retMess)
s.close()

s = socket(AF_INET, SOCK_STREAM)
s.connect((serverName, 12302))
print("Connected")
l = json.dumps((8.775, 32.2025, 30.6105))
s.send(l.encode())
retMess = s.recv(1024).decode()
print(retMess)
s.close()
