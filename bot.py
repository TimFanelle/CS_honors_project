towerIP = {'Tower1': "192.168.5.1", 'Tower2': '192.168.4.1'}
towerUUID = {'Tower1': '1bde4d5b-d112-4d24-bfac-3c43a9add89b', 'Tower2': '28149287-b18c-4b7d-9baf-c0a9fb824b59'}
towerLoc = {'Tower1': (0,0), 'Tower2': (10,0)}
degree = 0  # this is used for later

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import json
import serial

from socket import *

import cv2

def depthMapping():
	cap0 = cv2.VideoCapture(0)
	_, left = cap0.read()
	cap0.release()
	#print(left.shape)

	cap1 = PiCamera()
	cap1.resolution = (640, 480)
	cap1.framerate = 10
	cap1.brightness = 65

	rawC = PiRGBArray(cap1, size=(640, 480))
	time.sleep(0.1)
	cap1.capture(rawC, format="bgr")
	right = rawC.array
	
	#print(right.shape)

	right = cv2.flip(right, -1)
	left = cv2.flip(left, -1)

	stereo = cv2.StereoBM_create()
	stereo.setMinDisparity(3)
	stereo.setNumDisparities(16)
	stereo.setBlockSize(13)
	stereo.setSpeckleRange(17)
	stereo.setSpeckleWindowSize(19)

	gLeft = cv2.cvtColor(lPix, cv2.COLOR_RGB2GRAY)
	gRight = cv2.cvtColor(rPix, cv2.COLOR_RGB2GRAY)

	disparity = stereo.compute(gLeft, gRight)

	return disparity


def getRSSIs():
	outs = {'t1':0, 't2':0, 't3':0}
	
	#below this is correct code
	for i in range(1,2):
		connect2Tower(i)
		
		cmd = "iwconfig"
		outtie = subprocess.Popen(cmd, stdout=subprocess.PIPE)
		output, error = outs.communicate()
		output = output.decode()
		rssi = int(((output.split('\n')[5]).split("Signal level=")[1]).split()[0])
		outs['t' + str(i)] = rssi
	return (outs['t1'], outs['t2'])
	

def getLoc(rssiDistances):
	dist = []
	for i in rssiDistances:
		dist.append(math.pow(10, (-31 - i)/(10*1.6)))
	locX = ((dist[1]-dist[0])- math.pow(towerLoc["Tower2"][0], 2))/(-2*towerLoc["Tower2"][0])
	locY = math.sqrt(math.pow(dist[0], 2) - math.pow(locX, 2))
	return (locX, locY)


def connect2Tower(towerNum):
	cmd0 = "nmcli connection up uuid " + towerUUID[towerNum]
	out = subprocess.Popen(cmd0, stdout=subprocess.PIPE)
	output, error = outs.communicate()


def send2Tower(towerPort, towerNum=0, item=None):
	if towerPort == 18 and item is None:
		towerGetRssi = getRSSIs()
		print(towerGetRssi)
		thisLoc = getLoc(towerGetRssi)
		print(thisLoc)
		return
	
	connect2Tower(towerNum)
	
	sN = towerIP["Tower" + str(towerNum)]
	sP = towerPort
	
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((sN, sP))
	
	if towerPort == 16:
		listed = item.tolist()
		jListed = json.dumps(listed)
		clientSocket.send(jListed)
		
		retMess = clientSocket.recv(1024).decode()
		clientSocket.close()
		print(retMess)
		
	elif towerPort == 17:
		clientSocket.close()
		eloquint = getLoc(getRSSIs())
		connect2Tower(towerNum)
		toSend = str(eloquint[0])+";"+ str(elequint[1])+";" +str(degree)
		#j2Send = json.dumps(toSend)
		
		sN = towerIP["Tower" + str(towerNum)]
		sP = towerPort
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect((sN, sP))
		
		clientSocket.send(toSend)
		retMess = clientSocket.recv(1024).decode()
		clientSocket.close()
		print(retMess)
	
	return


def getDirs(endXY):
	eloquint = getLoc(getRSSIs())
	
	connect2Tower(1)
	
	sN = towerIP["Tower" + str(towerNum)]
	sP = 18
	
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((sN, sP))
	
	toSend = str(eloquint[0])+";"+ str(elequint[1])+";" +str(degree)+";"+str(endXY[0])+";"+str(endXY[1])
	clientSocket.send(toSend)
	retMess = clientSocket.recv(1024).decode()
	# retMess will be a list of instructions for the bot separated by semicolons
	clientSocket.close()
	#print(retMess)
	# convert string of retMess into an actual list and return it
	wattaMess = retMess.split(';')
	return wattaMess


def move(directions):
	ser=serial.Serial('/dev/ttyACM0', 96) #replace /dev/ttyACM4 with actual COM port from arduino
	#read directions and adjust degree accordingly
	ser.write(directions)
	if directions[0] == 'L' or directions[0] == 'R':
		readd = float(directions[1:])
		degree = degree + readd
		if degree >= 360:
			degree = degree - 360


def runPoint():
	xx =  input("X: ")
	yy =  input("Y: ")
	while 1:
		try:
			dispp = depthMapping()
			send2Tower(16, 1, dispp)
			send2Tower(17, 1)
			dirs = getDirs((xx,yy)) #arbitrary value for now
			for d in dirs:
				move(d)
		except:
			print("Error code 19")
	#things don't happen anymore
	

def runVacuum():
	#go for every point in the map


runPoint()
