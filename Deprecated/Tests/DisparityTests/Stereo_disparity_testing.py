import _pickle as cPickle
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
#uu = np.load('outpointsB.npy')
#uu = np.load('disparitttty.npy')
#print(uu.shape)

##############################################################3

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
stereo.setMinDisparity(17)
stereo.setNumDisparities(128)
stereo.setBlockSize(13)
stereo.setSpeckleRange(13)
stereo.setSpeckleWindowSize(21)

gLeft = cv2.cvtColor(lPix, cv2.COLOR_RGB2GRAY)
gRight = cv2.cvtColor(rPix, cv2.COLOR_RGB2GRAY)

cv2.imshow("left", gLeft)
cv2.imshow("right", gRight)

disparity = stereo.compute(gLeft, gRight)
cv2.imshow("disp", disparity.astype('uint8')*255)

while 1:
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
#cv2.destroyAllWindows()

Q =  sCalibration['Q']
threeDImage = cv2.reprojectImageTo3D(disparity, Q)
print(threeDImage.shape)
threeDImage = cv2.perspectiveTransform(threeDImage, Q)
print(threeDImage.shape)

###############################################################
#print(uu)
X = []
Y = []
Z = []
jr = 0
for i in threeDImage:
	for j in i:
		#print(str(j[0]) + "\t"+str(j[1])+"\t"+str(j[2]))
		if jr % 40 == 0:
			X.append(j[0])
			Y.append(j[1])
			Z.append(j[2])
		jr += 1

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X, Y, Z, c='r', marker='o')

ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')

plt.show()
