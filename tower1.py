from socket import *
import json
import numpy as np
import select
from warnings import warn

import cv2

sCalibration = np.load('matricesAnd.npz', allow_pickle=False)
transMatrix = [-20.9115, -14.431, 4/5]
recentLoad = None
heldMap = [[[0 for height in range(100)]for col in range(1000)]for row in range(1000)] #represented in cm X->10m; Y->10m; Z->1m;

ports = [16, 17, 18, 19]


def make_socket(number):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind(('', number))
	sock.listen(2)
	return sock


def project(q, disp):
	f_x = q[0, 0]
	f_y = q[1, 1]
	c_x = q[0, 2]
	c_y = q[1, 2]
	
	result = []
	for i in range(disp.shape[0]):
		for j in range(disp.shape[1]):
			#Z = #depth TODO: THIS
			X = (x  - 319.5 - c_x) / f_x * Z
			Y = (y - 319.5 - c_y) / f_y * Z
	result.append([X, Y, Z])
	return result


def reconst(towerSocket):
	connectionSocket = towerSocket
	try:
		data = connectionSocket.recv(1024)
		data = json.loads(data)
		data = np.asarray(data)
		
		#data0 = connectionSocket.recv(1024)
		
		Q =  sCalibration['Q']
		
		threeDpoints = project(Q, data)
		
		#threeDImage = cv2.reprojectImageTo3D(data, Q)
		#print(threeDImage.shape)
		#threeDImage = cv2.perspectiveTransform(threeDImage, Q)
		
		connectionSocket.send("Image received".encode())
		#recentLoad = threeDImage  # wait for 
		recentLoad = threeDpoints
		# place it in the model, or save it and use port 17 to get location and degree for placement
		
	except IOError:
		connectionSocket.send("\nError Code 6\n".encode())
		connectionSocket.close()
	connectionSocket.close()

def getCenterLine(X, Y, angle):
	slope = round(math.tan(math.pi*angle/180), 7)
	def outFunc(x):
		return (slope * (x - X)) + Y
	return outFunc


def placing2Map(towerSocket):
	connectionSocket = towerSocket
	try:
		data = connectionSocket.recv(1024).decode()
		#data = json.loads(data)
		apart = data.split(";")
		loc = (float(apart[0])*100, float(apart[1])*100)
		deg = float(apart[2])
		
		#print(data)
		
		connectionSocket.send("placement received".encode())
		
		# place recentLoad into heldMap based on location and degree
		centerLine = getCenterLine(loc[0], loc[1], deg)
		#perpLine = getCenterLine(Z, centerline(Z), deg+90)
		
		# THIS 100% HAS TO BE CHECKED
		# ALSO ONLY TELLS YOU IF SOMETHING IS THERE NOT IF SOMETHING ISN'T
		for xyz in recentLoad:
			X, Y, Z = xyz
			perpLine = getCenterLine(Z, centerline(Z), deg+90)
			HeldMap[loc[0], Y, loc[1] + perpLine(X)] = 1
			
	
	except IOError:
		connectionSocket.send("\nError Code 8\n".encode())
		connectionSocket.close()
	connectionSocket.close()

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, allow_diagonal_movement = False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    
    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze) + len(maze[0]) // 4) ** 2

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1
        
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            warn("giving up on pathfinding too many iterations")
            return return_path(current_node)

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []
        
        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0 and node_position != end:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            open_list.append(child)


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


def detDir(path, l, degree):
	par0 = path[0]
	par1 = path[1]
	par0_x, par0_y = par0
	par1_x, par1_y = par1
	dir = 0
	trial = [(-1,0),(0,-1),(1,0),(0,1)]
	if par0_x - par1_x <0:
		dir = 0
	elif par0_x - par1_x >0:
		dir = 2
	elif par0_y - par1_y <0:
		dir = 1
	else:
		dir = 3
	same = True
	dist = 1
	while same:
		testX = path[dist-1][0]-path[dist][0]
		testY = path[dist-1][1]-path[dist][1]
		if testX == trial[dir][0] and testY == trial[dir][1]:
			dist +=1
		else:
			same = False
	
	parEnd = path[dist]
	parEnd_x, parEnd_y = parEnd
	#trueDist = abs((((par0_x-parEnd_x) + (par0_y-parEnd_y))*l)/100)
	trueDist = ((dist-1)*l)/100

	expDeg = (dir * 90)
	delt = expDeg - degree
	d = 'L'
	outer = ""
	if 0 <=delt<= 180:
		outer = d + str(delt)
	elif -180 < delt <= 0:
		outer = 'R' + str(abs(delt))
	else:
		newDelt = (360 + degree)-expDeg
		outer = 'R' + str(abs(newDelt))
	
	if delt != 0:
		return outer + ";" + "F" + str(trueDist)
	else:
		return 'F' + str(trueDist)
	
	
def putItTogether(start, end, degree):
	inn = []
	for i in range(0, len(heldMap)):
		inn.append([])
		for j in range(0, len(heldMap[i])):
			inn[i].append(heldMap[i][j][:14])
	
	mip, startXY, endXY = modMap(inn, 19, start, end)
	path = astar(mip, startXY, endXY)
	out = detDir(path, 19, degree)
	return out



def giveDir(towerSocket):
	connectionSocket = towerSocket
	try:
		data = connectionSocket.recv(1024).decode()
		apart = data.split(";")
		
		loc = (float(apart[0]*100), float(apart[1])*100)
		deg = float(apart[2])
		endLoc = (float(apart[3])*100, float(apart[4])*100)
		
		#path = astar(heldMap, (loc[0], loc[1]), (endLoc[0], endLoc[1]))
		retInstr = putItTogether(loc, endLoc, deg)
		#run a route finding algorithm to get from loc to endLoc and send the first 3-4 steps over
		connectionSocket.send("Route Created".encode())
		connectionSocket.close()
	except IOError:
		connectionSocket.send("\nError Code 9\n".encode())
		connectionSocket.close()
	connectionSocket.close()

def undef(dontMatter):
	return 0
	

read_list = list(map(lambda x: make_socket(x), ports))
notAccepted = read_list[:]
choices = {16: reconst, 17: placing2Map, 18: giveDir, 19: undef}
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
			print(address[0])
			choices[port]((address[0], clientSocket))
			read_list.remove(clientSocket)