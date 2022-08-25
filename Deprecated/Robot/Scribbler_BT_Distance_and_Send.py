# from socket import *
import bluetooth
from PIL import Image
import numpy as np
import zipfile
import json
import os


hosts = {'Scribbler': '00:1E:19:01:06:04', 'Tower1': "B8:27:EB:1D:42:35", 'Tower2': ''} #'B8:27:EB:93:F7:AF', 'Tower3': ''}  # IPRE6-245426

serverName = hosts['Tower1']
serverPort = 16
f0 = 'Resources/IMG0.JPG'
f1 = 'Resources/IMG1.JPG'
f2 = 'Resources/IMG2.JPG'
f3 = 'Resources/IMG3.JPG'


def sDat(sN, sP, dd):
	clientSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
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
	# clientSocket.shutdown(1)
	retMes = clientSocket.recv(1024).decode()
	print(retMes)
	clientSocket.close()


def getRSSIs():
	outs = {'t1':0, 't2':0, 't3':0}
	for i in range(1, 3):
		s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		s.connect((hosts['Tower'+str(i)], 18))
		outs['t'+str(i)] = json.loads(s.recv(1024).decode())
		s.close()
	return (outs['t1'], outs['t2'], outs['t3'])
		

sDat(serverName, serverPort, Image.open(f2))
sDat(serverName, serverPort, Image.open(f3))
sDat(serverName, serverPort, "Clear")

quarter = getRSSIs()
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverName, 17))
print("Connected")
#l = json.dumps((25.573, 38.131, 13.191))
quarter = json.dumps(quarter)
#s.send(l)
s.send(quarter)
retMess = s.recv(1024).decode()
print(retMess)
s.close()
