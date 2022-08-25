"""
* Check for config file
*	if none then configure
*	else check for configured Bool
*		if false then configure
*		else move to either mapping until navigation signal is sent
"""

#Configuration startup
"""
1. take picture (send to T1) 
2. move .5 meters forward
3. take picture (send to T1)
4. receive distance between
5. configure focal and update config file
"""


#Mapping startup
#assume facing 0 degrees


#Navigationg startup
"""
1. determine end location and current position/angle
2. send information to T2 for routing
3. receive instructions
4. compile as robot movement commands
5. execute and take mind of unforseen obstacles
6. repeat
"""


#ignore everything above this
towers = {'Tower1': "B8:27:EB:1D:42:35", 'Tower2': 'B8:27:EB:1D:9F:31'} #  put tower information here
towerLoc = {'Tower1': (0,0), 'Tower2': (10,0)}
degree = 0  # this is used for later

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import json
import bluetooth

from socket import *

import cv2

def depthMapping():
	cap0 = cv2.VideoCapture(0)
	_, left = cap0.read()
	cap0.release()
	print(left.shape)

	cap1 = PiCamera()
	cap1.resolution = (1280, 720)
	cap1.framerate = 10
	cap1.brightness = 65

	rawC = PiRGBArray(cap1, size=(1280, 720))
	time.sleep(0.1)
	cap1.capture(rawC, format="bgr")
	right = rawC.array
	
	#TODO: apply pre-filtering and sizing

	right = right[0:720-240, 320:1280-320]
	print(right.shape)

	right = cv2.flip(right, -1)
	rawC.truncate()

	stereo = cv2.StereoBM_create()
	stereo.setMinDisparity(13)
	stereo.setNumDisparities(80)
	stereo.setBlockSize(7)
	stereo.setSpeckleRange(13)
	stereo.setSpeckleWindowSize(50)

	gLeft = cv2.cvtColor(left, cv2.COLOR_RGB2GRAY)
	gRight = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

	disparity = stereo.compute(gLeft, gRight)

	#cv2.imshow("disparity", disparity.astype('uint8')*255)
	return disparity


def getRSSIs():
	outs = {'t1':0, 't2':0, 't3':0}
	for i in range(1, 3):
		s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		s.connect((towers['Tower'+str(i)], 18))
		outs['t'+str(i)] = json.loads(s.recv(1024).decode())
		s.close()
	return (outs['t1'], outs['t2'])  # , outs['t3'])
	
	#below this is correct code
	cmd = iwconfig
	outs = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	output, error = outs.communicate()
	output = output.decode()
	rssi = int(((output.split('\n')[5]).split("Signal level=")[1]).split()[0])
	print(rssi)
	

def getLoc(rssiDistances):
	dist = []
	for i in rssiDistances:
		dist.append(math.pow(10, (%defaultTransmitPower - i)/(10*1.6)))
	locX = ((dist[1]-dist[0])- math.pow(towerLoc["Tower2"][0], 2))/(-2*towerLoc["Tower2"][0])
	locY = math.sqrt(math.pow(dist[0], 2) - math.pow(locX, 2))
	return (locX, locY)


def send2Tower(towerPort, towerNum=0, item=None):
	if towerPort == 18 and item is None:
		towerGetRssi = getRSSIs()
		print(towerGetRssi)
		thisLoc = getLoc(towerGetRssi)
		print(thisLoc)
		return
	
	sN = towers["Tower" + str(towerNum)]
	sP = towerPort
	
	clientSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	clientSocket.connect((sN, sP))
	
	if towerPort == 16:
		listed = item.tolist()
		jListed = json.dumps(listed)
		clientSocket.send(jListed)
		
		#TODO: get perspective tranformation matrix and save to rq
		#rq = cv2.rectifyStereo(  # input things here
		#clientSocket.send(rq)  # change rq form to be able to send
		retMess = s.recv(1024).decode()
		s.close()
		print(retMess)
		
	return


goingOut = depthMapping()
send2Tower(16, 1, goingOut)
