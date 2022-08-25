# TODO: below
# adding height and width to distance output
# adjusting contouring to consider lines that reach the edge to contour across the edge until they reach another line

import cv2
import numpy as np
import queue_
from socket import *
import os
from PIL import Image
import select
import math
import json
import zipfile


ports = [1104, 12203, 12302, 12555, 12409]

towerLoc = [(0, 0, 0), (40, 0, 0), (20, 30, 0)]

lastIm = None

def maxCont(yy):
	m = yy[0]
	for u in yy:
		if cv2.contourArea(u) > cv2.contourArea(m):
			m = u
	return m


def WHCalc(dis, img, foc):  # something is off here
	# TODO: FIX THIS
	'''
	DIS = distance to object
	IMG = numpy array of image
	will return a tuple containing width and height of object
	'''

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	blur = cv2.blur(gray, (3, 3))
	ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_TOZERO)

	edge = cv2.Canny(thresh, 35, 90)

	contours, hierarchy = cv2.findContours(edge, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

	contOut = []
	minContourArea = 30
	for i in range(len(contours)):
		if cv2.contourArea(contours[i]) > minContourArea:
			contOut.append(contours[i])

	contOut = np.asarray(contOut)
	contOut = maxCont(contOut)

	rect = cv2.minAreaRect(contOut)

	box = cv2.boxPoints(rect)
	box = np.int0(box)
	cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

	x, y, widd, hi = cv2.boundingRect(contOut)

	# x, y, widd, hi = cv2.boundingRect(img)
	print(x)
	widd = (widd * dis)/(foc)
	hi = (hi * dis)/(foc)
	print(foc)
	print(widd)
	print(hi)
	return widd, hi


def detDist(w0, w1, trav):
	r = w1*trav
	d = r/(w1-w0)
	return round(d-trav, 3)


def runDets(img0, img1):
	images = [img0, img1]
	widAndPix = list()
	global lastIm
	lastIm= img1
	for img in images:
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		blur = cv2.blur(gray, (3, 3))
		ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_TOZERO)

		edge = cv2.Canny(thresh, 35, 90)

		# contours = []
		# hierarchy = []
		contours, hierarchy = cv2.findContours(edge, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

		contOut = []
		minContourArea = 30
		for i in range(len(contours)):
			if cv2.contourArea(contours[i]) > minContourArea:
				contOut.append(contours[i])

		contOut = np.asarray(contOut)
		contOut = maxCont(contOut)

		rect = cv2.minAreaRect(contOut)
		cent, lens, angl = rect
		# wid, heig = lens
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

		i = 0
		out = 0
		inn = 0
		x, y, widd, hi = cv2.boundingRect(contOut)

		widAndPix.append(widd)
		while i < contOut.shape[0]:
			rx, ry, w, h = cv2.boundingRect(contOut[i])
			if hierarchy[0][1].any() < 0:
				cv2.rectangle(img, (rx, ry), (rx + w, ry + h), (255, 0, 0), 2, 8, 0)
				out += 1
			else:
				cv2.rectangle(img, (rx, ry), (rx + w, ry + h), (0, 255, 0), 2, 8, 0)
				inn += 1
			i += 1

		cv2.drawContours(img, contOut, -1, (0, 255, 0), 3)
		# cv2.imshow("test", img)
		# while True:
			# if cv2.waitKey(1) & 0xFF == ord('q'):
				# break

	travelled = 5
	dist = detDist(widAndPix[0], widAndPix[1], travelled)
	# print("Currently " + str(dist) + " from object")
	# cv2.destroyAllWindows()

	return str(dist)


def trilatHelp(centers, t1r, t2r, t3r):  # look into this
	t1c = centers[0]
	t2c = centers[1]
	t3c = centers[2]

	x = -1 * (math.pow(t1r, 2) - math.pow(t2r, 2) + math.pow(t2c[0], 1))/(2*t2c[0])
	y = (math.pow(t1r, 2) - math.pow(t3r, 2) + (math.pow(t3c[0], 2)+math.pow(t3c[1], 2)) - (2*t3c[0]*x))/(2*t3c[1])
	try:
		z = math.sqrt(math.pow(t1r, 2) - math.pow(x, 2) - math.pow(y, 2))
	except ValueError:
		z = math.sqrt(-1*(math.pow(t1r, 2) - math.pow(x, 2) - math.pow(y, 2)))

	return x, y, z


def make_socket(number):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	sock.bind(('', number))
	sock.listen(2)
	return sock


def imgProc(towerSocket):
	# connectionSocket, addr = towerSocket.accept()
	try:
		f = open("temp.ccr")
		f.close()
		os.remove("temp.ccr")
		print("file deleted")
	except FileNotFoundError:
		badVar = 1

	connectionSocket = towerSocket
	try:
		l = connectionSocket.recv(1024)
		if l.__sizeof__() < 30:
			quiggle.push("Clear")
		else:
			femp = open("temp.ccr", 'wb')

			while l:
				femp.write(l)
				if l.__sizeof__() < 1024:
					break
				l = connectionSocket.recv(1024)

			# focal = json.loads(connectionSocket.recv(1024).decode())

			# message = connectionSocket.recv(1024)
			# message = np.frombuffer(message)
			# print(focal.__sizeof__())
			# print(focal)
			femp.close()
			fem = Image.open('temp.ccr')
			message = np.asarray(fem)
			fem.close()
			os.remove("temp.ccr")
			quiggle.push(message)
		if len(quiggle) > 1:
			out = quiggle.pop().getDat()
			o1 = quiggle.peek().getDat()
			if not isinstance(o1, np.ndarray):
				quiggle.pop()
				retMes = "Received Code 01"
				connectionSocket.send(retMes.encode())
				connectionSocket.close()
			else:
				retMes = runDets(out, o1)
				connectionSocket.send(retMes.encode())
				connectionSocket.close()
		else:
			connectionSocket.send("Awaiting Second Image".encode())
			connectionSocket.close()
	except IOError:
		connectionSocket.send("\nError Code 6\n".encode())
		connectionSocket.close()
	connectionSocket.close()


# this is probably going to be changed to work with 2 towers and the third is a check
# TODO: Write as 2 towers with check tower
def trilat(cSocket):
	try:
		data = cSocket.recv(1024)
		data = json.loads(data.decode())
		ending = trilatHelp(towerLoc, data[0], data[1], data[2])
		print(ending)
		out = json.dumps(ending)
		cSocket.send(out.encode())
	except IOError:
		cSocket.send("\nError Code 6\n".encode())
		cSocket.close()
	cSocket.close()


def focWidHit(towerSocket):
	try:
		data = towerSocket.recv(1024)
		data = json.loads(data.decode())
		focal = data[0]
		dist = data[1]
		wid, height = WHCalc(dist, lastIm, focal)
		print(wid, height)
		out = json.dumps((wid, height))
		towerSocket.send(out.encode())
	except IOError:
		towerSocket.send("\nError Code 6\n".encode())
		towerSocket.close()
	towerSocket.close()


def rssI(cSocket):
	# will be written on raspi
	return 0


def undef(dontMatter):
	return 0


read_list = list(map(lambda x: make_socket(x), ports))
notAccepted = read_list[:]
quiggle = queue_.queue_()
choices = {1104: focWidHit, 12203: imgProc, 12302: trilat, 12555: rssI, 12409: undef}
while True:
	print("ready to serve")
	readable, writable, errored = select.select(read_list, [], [])
	for s in readable:
		if s in notAccepted:
			clientSocket, address = s.accept()
			port = s.getsockname()[1]
			read_list.append(clientSocket)
			print("connection on port: ", port)
			print("performing ", choices[port])
			choices[port](clientSocket)
			read_list.remove(clientSocket)
