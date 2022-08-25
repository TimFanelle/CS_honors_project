import cv2
import numpy as np
import queue_
# from socket import *
import os
from PIL import Image
import bluetooth

# dv = bluetooth.discover_devices(duration=3, lookup_names=True)
# print(dv)


def maxCont(yy):
	m = yy[0]
	for u in yy:
		if cv2.contourArea(u) > cv2.contourArea(m):
			m = u
	return m


def detDist(w0, w1, trav):
	r = w1*trav
	d = r/(w1-w0)
	return round(d-trav, 3)


def runDets(img0, img1):
	images = [img0, img1]
	widAndPix = list()
	for img in images:
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		blur = cv2.blur(gray, (3, 3))
		ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_TOZERO)

		edge = cv2.Canny(thresh, 35, 90)

		contours, hierarchy = cv2.findContours(edge, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

		contOut = []
		minContourArea = 600
		for i in range(len(contours)):
			if cv2.contourArea(contours[i]) > minContourArea:
				contOut.append(contours[i])

		contOut = np.asarray(contOut)
		contOut = maxCont(contOut)

		rect = cv2.minAreaRect(contOut)
		cent, lens, angl = rect
		wid, heig = lens
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
	dist = detDist(widAndPix[0], widAndPix[1], 5)
	return str(dist)


serverPort = 13
towerSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

towerSocket.bind(('', serverPort))
towerSocket.listen(1)

quiggle = queue_.queue_()
while True:
	print("serving...")
	connectionSocket, addr = towerSocket.accept()
	try:
		l = connectionSocket.recv(1024)
		if l.__sizeof__() < 30:
			quiggle.push("Clear")
		else:
			femp = open("temp.ccr", 'wb')
			while l:
				femp.write(l)
				l = connectionSocket.recv(1024)
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
towerSocket.close()
