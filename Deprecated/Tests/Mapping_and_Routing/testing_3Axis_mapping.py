import cv2
import numpy as np


def gDisp(left, right):
    barnL = np.load(left)
    barnR = np.load(right)

    lPix = barnL
    rPix = barnR

    print(lPix.shape)
    print(rPix.shape)

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


def fromDisp(disp):
	Q = sCalibration['Q']
	out = cv2.reprojectImageTo3D(disp, Q)
	out = cv2.perspectiveTransform(out, Q)
	out = out.reshape((-1, 3))
	out = modZ(out)
	return out

d0 = np.flip(gDisp('left.npy', 'right.npy'), -1)
d1 = np.flip(gDisp('left1.npy', 'right1.npy'), -1)
sCalibration = np.load('checkMatrices0.npz', allow_pickle=False)

#Q = sCalibration['Q']
threeDImage0 = fromDisp(d0)
threeDImage1 = fromDisp(d1)
#threeDImage1 = cv2.reprojectImageTo3D(d1, Q)
#print(threeDImage1.shape)
#threeDImage1 = cv2.perspectiveTransform(threeDImage1, Q)
#print(threeDImage1.shape)

print("completed points")

#xyz = threeDImage0.reshape((-1, 3))
#xyz0 = threeDImage1.reshape((-1, 3))


def rangess(uu):
    rminx = uu[0][0]
    rmaxx = uu[0][0]
    rminy = uu[0][1]
    rmaxy = uu[0][1]
    rminz = uu[0][2]
    rmaxz = uu[0][2]
    for yy in uu:
        if yy[0] < rminx:
            rminx = yy[0]
        elif yy[0] > rmaxx:
            rmaxx = yy[0]
        if yy[1] < rminy:
            rminy = yy[1]
        elif yy[1] > rmaxy:
            rmaxy = yy[1]
        if yy[2] < rminz:
            rminz = yy[2]
        elif yy[2] > rmaxz:
            rmaxz = yy[2]
    rx = rmaxx-rminx
    ry = rmaxy-rminy
    rz = rmaxz-rminz
    return rx, ry, rz

def modZ(uu):
    cz = []
    for yy in uu:
        cz.append(yy[2])
    maxx = cz[0]
    for qqq in cz:
        if qqq > maxx:
            maxx = qqq
    out = []
    jj = uu.reshape((-1))
    jj = np.delete(jj, np.argwhere(jj == 32) - 2)
    jj = np.delete(jj, np.argwhere(jj == 32) - 1)
    jj = np.delete(jj, np.argwhere(jj == 32))
    jj = np.delete(jj, np.argwhere(jj >= 256) - 2)
    jj = np.delete(jj, np.argwhere(jj >= 256) - 1)
    jj = np.delete(jj, np.argwhere(jj >= 256))
    jj = jj.reshape((-1, 3))

    for yy in jj:
        yy[0] = yy[0]*(-20.9115)
        yy[1] = yy[1]*(-14.431)
        yy[2] = yy[2]*(4/5)
    uu = jj
    return uu


print('xyz')
xyz = modZ(xyz)
r0 = rangess(xyz)
print(xyz.shape)
print(r0)

print('xyz0')
xyz0 = modZ(xyz0)
print(xyz0.shape)
r1 = rangess(xyz0)
print(r1)

