import cv2
from PIL import ImageGrab as ig
import numpy as np

bb = (40, 10, 630, 700)
while True:
	img = np.array(ig.grab(bb))
	print(img.size)
	img = cv2.convertScaleAbs(img, None, 1.3, 47)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	blur = cv2.blur(gray, (3, 3))
	ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_TOZERO)

	edge = cv2.Canny(thresh, 35, 90)

	contours = []
	hierarchy = []
	contours, hierarchy = cv2.findContours(edge, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	#print(len(contours))
	#print(len(hierarchy[0]))

	contOut = []
	minContourArea = 420
	for i in range(len(contours)):
		if cv2.contourArea(contours[i]) > minContourArea:
			contOut.append(contours[i])

	contOut = np.asarray(contOut)
	i = 0
	out = 0
	inn = 0
	while i < contOut.shape[0]:
		rx, ry, w, h = cv2.boundingRect(contOut[i])
		#print(hierarchy[i][2])
		if hierarchy[0][1].any() < 0:
			cv2.rectangle(img, (rx, ry), (rx + w, ry + h), (255, 0, 0), 2, 8, 0)
			out += 1
		else:
			cv2.rectangle(img, (rx, ry), (rx + w, ry + h), (0, 255, 0), 2, 8, 0)
			inn += 1
		i += 1#hierarchy[i][0]
	#print(out)
	print((inn-1)//2)# this is wrong

	#print(len(contOut))

	#cv2.drawContours(img, contOut, -1, (0, 255, 0), 3)

	#contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#hull = []
	#for i in range(len(contours)):
	#	hull.append(cv2.convexHull(contours[i], False))

	#drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
	#for i in range(len(contours)):
	#	color_contours = (0, 255, 0)
	#	color = (255, 0, 0)
	#	cv2.drawContours(drawing, contours, i, color_contours, 1, 8, hierarchy)
	#	cv2.drawContours(drawing, hull, i, color, 1, 8)
	#print(len(contours))
	cv2.imshow("test", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows()
