import cv2
import numpy as np

CHESSBOARD_SIZE = (14, 10)
CHESSBOARD_OPTIONS = (cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_FAST_CHECK)
OBJECT_POINT_ZERO = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
OBJECT_POINT_ZERO[:,:2] = NP.MGRID[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1,2)

TERMINATION_CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

OPTIMIZE_ALPHA = 0.2

# capture images
cap0 = cv2.VideoCapture(0)
_, left = cap0.read()
cap0.release()
print(left.shape)

cap1 = PiCamera()
cap1.resolution = (640, 480)
cap1.framerate = 10
cap1.brightness = 65

rawC = PiRGBArray(cap1, size=(640, 480))
time.sleep(0.1)
cap1.capture(rawC, format="bgr")
right = rawC.array

#TODO: apply pre-filtering and sizing

#right = right[0:720-240, 320:1280-320]
print(right.shape)

right = cv2.flip(right, -1)
left = cv2.flip(left, -1)
#rawC.truncate()

imgL = left
imgR = right
	
# calibrate cameras

imgLG = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
imgRG = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

imgSize = imgLG.shape[::-1]

objectPointsL = []
objectPointsR = []
imagePointsL = []
imagePointsR = []

hascornersL, cornersL = cv2.findChessboardCorners(imgLG, CHESSBOARD_SIZE, cv2.CALIB_CB_FAST_CHECK)
hascornersR, cornersR = cv2.findChessboardCorners(imgRG, CHESSBOARD_SIZE, cv2.CALIB_CB_FAST_CHECK)

if hascornersL:
	objectPointsL.append(OBJECT_POINT_ZERO)
	cv2.cornerSubPix(imgLG, cornersL, (11,11), (-1,-1), TERMINATION_CRITERIA)
	imagePointsL.append(cornersL)
	
	cv2.drawChessboardCorners(imgL, CHESSBOARD_SIZE, cornersL, hascornersL)
	cv2.imshow(imageD, imgL)

if hascornersR:
	objectPointsR.append(OBJECT_POINT_ZERO)
	cv2.cornerSubPix(imgRG, cornersR, (11,11), (-1,-1), TERMINATION_CRITERIA)
	imagePointsR.append(cornersR)
	
	cv2.drawChessboardCorners(imgR, CHESSBOARD_SIZE, cornersR, hascornersR)
	cv2.imshow(imageD, imgR)

print("Calibrating left camera...")
_, leftCameraMatrix, leftDistortionCoefficients, _, _ = cv2.calibrateCamera(objectPointsL, imagePointsL, imgSize, None, None)
print("Calibrating right camera...")
_, rightCameraMatrix, rightDistortionCoefficients, _, _ = cv2.calibrateCamera(objectPointsL, imagePointsR, imgSize, None, None)

print("Calibrating cameras together...")
(_, _, _, _, _, rotationMatrix, translationVector, _, _) = cv2.stereoCalibrate(objectPointsL, imagePointsL, imagePointsR, leftCameraMatrix, leftDistortionCoefficients, rightCameraMatrix, rightDistortionCoefficients, imgSize, None, None, None, None, cv2.CALIB_FIX_INTRINSIC, TERMINATION_CRITERIA)

(leftRectification, rightRectification, leftProjection, rightProjection, disparityToDepthMap, leftROI, rightROI) = cv2. stereoRectify(leftCameraMatrix, leftDistortionCoefficients, rightCameraMatrix, rightDistortionCoefficients, imgSize, rotationMatrix, translationVector, None, None, None, None, None, cv2.CALIB_ZERO_DISPARITY, OPTIMIZE_ALPHA)

leftMapX, leftMapY = cv2.initUndistortRectifyMap(leftCameraMatrix, leftDistortionCoefficients, leftRectification, leftProjection, imgSize, cv2.CV_32FC1)
rightMapX, rightMapY = cv2.initUndistortRectifyMap(rightCameraMatrix, rightDistortionCoefficients, rightRectification, rightProjection, imgSize, cv2.CV_32FC1)

np.savez_compressed('matricesAnd', imageSize=imgSize, leftMapX=leftMapX, leftMapY=leftMapY, leftROI=leftROI, rightMapX=rightMapX, rightMapY=rightMapY, rightROI=rightROI, rotMatrix=rotationMatrix, transVector=translationVector, Q=disparityToDepthMap)