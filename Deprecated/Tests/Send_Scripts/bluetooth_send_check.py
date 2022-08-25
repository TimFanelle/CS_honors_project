# from socket import *
import bluetooth
from PIL import Image
import numpy as np
import json
import os


hosts = {'bravenNum': '10:B7:F6:0A:69:F9', 'sNum': 'D0:92:9E:82:A7:59', 'Scribbler': '00:1E:19:01:06:04', 'Tower1': "B8:27:EB:1D:42:35", 'test': 'AA:45:23:89:E4:C5'}  # BRAVEN 704, Stephany, IPRE6-245426

serverName = hosts['Tower1']
serverPort = 16
f0 = 'Resources/IMG0.JPG'
f1 = 'Resources/IMG1.JPG'


def sDat(sN, sP, dd):
	clientSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	clientSocket.connect((sN, sP))

	if not isinstance(dd, str):
	#	dd.save('t.png')
	#	tempp = open('t.png', 'rb')
	#	l = tempp.read(1024)
	#	while l:
	#		clientSocket.send(l)
	#		l = tempp.read(1024)
		sened = json.dumps(dd)
		clientSocket.send(sened)
		print("File Sent")
		#tempp.close()
	#	os.remove('t.png')
	else:
		tempp = "Clear".encode()
		clientSocket.send(tempp)
		print("Code 01 Sent")
	# clientSocket.shutdown(1)
	retMes = clientSocket.recv(1024).decode()
	print(retMes)
	clientSocket.close()


sDat(serverName, serverPort, Image.open(f0))
sDat(serverName, serverPort, Image.open(f1))
sDat(serverName, serverPort, "Clear")
