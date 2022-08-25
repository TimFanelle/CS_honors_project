import cv2
import numpy as np
from PIL import Image


barnL = np.load('left.npy')
barnR = np.load('right.npy')
sCalibration = np.load('checkMatrices.npz', allow_pickle=False)

lPix = barnL
rPix = barnR

print(lPix.shape)
print(rPix.shape)

stereo = cv2.StereoBM_create()
stereo.setMinDisparity(7)
stereo.setNumDisparities(96)
stereo.setBlockSize(5)
stereo.setSpeckleRange(11)
stereo.setSpeckleWindowSize(18)

gLeft = cv2.cvtColor(lPix, cv2.COLOR_RGB2GRAY)
gRight = cv2.cvtColor(rPix, cv2.COLOR_RGB2GRAY)

cv2.imshow("left", gLeft)
cv2.imshow("right", gRight)

disparity = stereo.compute(gLeft, gRight)
cv2.imshow("disp", disparity.astype('uint8')*255)

while 1:
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows()

Q =  sCalibration['Q']
threeDImage = cv2.reprojectImageTo3D(disparity, Q)
print(threeDImage.shape)
threeDImage = cv2.perspectiveTransform(threeDImage, Q)
print(threeDImage.shape)

print("here")

for i in threeDImage:
	for j in i:
		print(j)