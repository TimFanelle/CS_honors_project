import math
#import scipy as sp
#def gCirD(latA, longA, latB, longB):
#	phi1 = math.radians(latA)
#	lam1 = math.radians(longA)
#
#	phi2 = math.radians(latB)
#	lam2 = math.radians(longB)
#
#	delt_lamb = math.fabs(lam2-lam1)
#
#	central_angle = math.atan2(math.sqrt(math.pow(math.cos(phi2)*math.sin(delt_lamb), 2.0) + math.pow(math.cos(phi1)*math.sin(phi2)-math.sin(phi1)*math.cos(phi2)*math.cos(delt_lamb), 2.0)), (math.sin(phi1)*math.sin(phi2)+math.cos(phi1)*math.cos(phi2)*math.cos(delt_lamb)))
#
#	R = 6371.09  # km (needs to change)
#	return R*central_angle
#

#def mse(p, centers, distances):
#	mse = 0.0
#	for center, distance in zip(centers, distances):
#		distance_calc = gCirD(p[0], p[1], center[0], center[1])
#		mse += math.pow(distance_calc - distance, 2.0)
#	return mse / len(centers)


#result = #things





def trilat(centers, t1r, t2r, t3r):
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


c = [(0, 0, 0), (40, 0, 0), (20, 30, 0)]

print(trilat(c, 25.573, 38.131, 13.191))
