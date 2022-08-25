import cv2
import numpy as np
from PIL import Image


barnL = np.load('F:/499/left.npy')
barnR = np.load('F:/499/right.npy')
backBarn = np.load('F:/499/right_Backuped.npy')



#lPix = twoD2Arr(barnL)
#rPix = twoD2Arr(barnR)
lPix = barnL
rPix = barnR


#lPic = Image.open('F:/499/left_image.jpg')
#lPix = cv2.flip(np.array(lPic), -1)
#lPix = cv2.imread("F:/499/left_image.jpg")
print(lPix.shape)
#lPix = lPix[0:720-240, 0:640]
#print(lPix.shape)
#rPic = Image.open('F:/499/right_image.jpg')
#rPix = cv2.imread('F:/499/right_image.jpg')
#rPix = np.array(rPic)
print(rPix.shape)
cv2.imshow("pree", rPix)
#rPic = rPix[240:720, 640:1280]
#print(rPic.shape)

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

#cv2.imshow("left", lPix)
#cv2.imshow("right", rPic)

disparity = stereo.compute(gLeft, gRight)
cv2.imshow("disp", disparity.astype('uint8')*255)

while 1:
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows()
