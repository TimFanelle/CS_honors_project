
inn = [[[0]*140]*1000]*1000

starX = 71
starY = 93


def syphon(arr, l, start, end):
	if start > l and start + l < len(arr)-1:
		out = [(start - l, start + l)]
	else:
		out = []
	curL = start - (2*l)
	curR = start + (2*l)
	while curL >=0 or curR-l <= len(arr):
		if curL-l <= 0 and curR+l >= len(arr)-1:
			tried = 0
			try:
				if out[0][0] == 0:
					out = out + [(curR - l+1, len(arr) - 1)]
					tried = 1
			except IndexError:
				out = [(0, start)] + out + [(start+1, len(arr) - 1)]
				tried = 1
			try:
				if tried is not 1:
					if out[len(out) - 1][1] == len(arr) - 1 and tried is not 1:
						out = [(0, curL + l - 1)] + out
						tried = 1
			except IndexError:
				out = [(0, curL + l - 1)] + out + [(start, len(arr) - 1)]
				tried = 1
			if tried is not 1:
				out = [(0, curL + l - 1)] + out + [(curR - l + 1, len(arr) - 1)]
		elif curL-l > 0 and curR+l >= len(arr)-1:
			if curR - l > len(arr)-1:
				try:
					if out[len(out)-1][1] == len(arr)-1:
						out = [(curL - l, curL + l - 1)] + out
				except IndexError:
					out = [(curL - l, curL + l - 1)] + out + [(start-l, len(arr) - 1)]
			else:
				out = [(curL-l, curL+l-1)] + out + [(curR-l+1, len(arr)-1)]
		elif curL-l <= 0 and curR+l < len(arr)-1:
			try:
				if out[0][0] == 0:
					out = out + [(curR-l+1, curR+l)]
				else:
					out = [(0, curL+l-1)] + out + [(curR-l+1, curR+l)]
			except IndexError:
				out = [(0, start+l)] + out + [(curR-l+1, curR+l)]
		else:
			out = [(curL-l, curL+l-1)] + out + [(curR-l+1, curR+l)]

		curL-= (2*l)
		curR += (2*l)
	out1 = 0
	out2 = 0
	for o in range(0, len(out)):
		oo, ooo = out[o]
		if ooo > start > oo:
			out1 = o
		if ooo > end > oo:
			out2 = o
	return out, out1, out2

def detOnes(arr, t, u, l):
	xs, xe = t
	ys, ye = u
	for i in range(xs, xe):
		for j in range(ys, ye):
			for k in range(0, len(arr[i][j])-1):
				if arr[i][j][k] == 1 or xe-xs < (2*l)-2 or ye-ys < (2*l)-2:
					return 1
	return 0


def modMap(arr, l, start, end=(-1, -1)):
	if end == (-1, -1):
		end = (3*l, 3*l)

	startX, startY = start
	endX, endY = end

	X, rx, qx = syphon(arr, l, startX, endX)
	Y, ry, qy = syphon(arr, l, startY, endY)
	preBuild = []
	for r in range(0, len(Y)):
		preBuild.append([])
		for s in range(0, len(X)):
			preBuild[r].append([X[s], Y[r]])
	build = []
	for b in range(0, len(preBuild)):
		build.append([])
		for z in range(0, len(preBuild[0])):
			build[b].append(detOnes(arr, preBuild[b][z][0], preBuild[b][z][1], l))
	return build, (rx, ry), (qx, qy)


#park, piff, puff = modMap(inn, 19, (starX, starY))
#for line in park:
#	print(line)
#print(piff)
#print(puff)

heldMap = [[[0 for height in range(100)]for col in range(1000)]for row in range(1000)]
print(len(heldMap), len(heldMap[0]), len(heldMap[0][0]))
hm = []
for i in range(0, len(heldMap)):
	hm.append([])
	for j in range(0, len(heldMap[i])):
		hm[i].append(heldMap[i][j][:14])

print(len(hm), len(hm[0]), len(hm[0][0]))
