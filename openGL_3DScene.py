# Import a library of functions called 'pygame'
from curses.ascii import SP
import pygame
import math
import numpy as np

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Point3D:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		
class Line3D():
	
	def __init__(self, start, end):
		self.start = start
		self.end = end

def loadOBJ(filename):
	
	vertices = []
	indices = []
	lines = []
	
	f = open(filename, "r")
	for line in f:
		t = str.split(line)
		if not t:
			continue
		if t[0] == "v":
			vertices.append(Point3D(float(t[1]),float(t[2]),float(t[3])))
			
		if t[0] == "f":
			for i in range(1,len(t) - 1):
				index1 = int(str.split(t[i],"/")[0])
				index2 = int(str.split(t[i+1],"/")[0])
				indices.append((index1,index2))
			
	f.close()
	
	#Add faces as lines
	for index_pair in indices:
		index1 = index_pair[0]
		index2 = index_pair[1]
		lines.append(Line3D(vertices[index1 - 1],vertices[index2 - 1]))
		
	#Find duplicates
	duplicates = []
	for i in range(len(lines)):
		for j in range(i+1, len(lines)):
			line1 = lines[i]
			line2 = lines[j]
			
			# Case 1 -> Starts match
			if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
				if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
					duplicates.append(j)
			# Case 2 -> Start matches end
			if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
				if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
					duplicates.append(j)
					
	duplicates = list(set(duplicates))
	duplicates.sort()
	duplicates = duplicates[::-1]
	
	#Remove duplicates
	for j in range(len(duplicates)):
		del lines[duplicates[j]]
	
	return lines

def loadHouse():
	house = []
	#Floor
	house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
	house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
	house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
	house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
	#Ceiling
	house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
	house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
	house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
	house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
	#Walls
	house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
	house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
	house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
	house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
	#Door
	house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
	house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
	house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
	#Roof
	house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
	house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
	house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
	house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
	house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))
	
	return house

def loadCar():
	car = []
	#Front Side
	car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
	car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
	car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
	car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
	car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
	car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

	#Back Side
	car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
	car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
	car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
	car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
	car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
	car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))
	
	#Connectors
	car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
	car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
	car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
	car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
	car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
	car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

	return car

def loadTire():
	tire = []
	#Front Side
	tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
	tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
	tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
	tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
	tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
	tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
	tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
	tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

	#Back Side
	tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
	tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
	tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
	tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
	tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
	tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
	tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
	tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

	#Connectors
	tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
	tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
	tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
	tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
	tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
	tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
	tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
	tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))
	
	return tire

	
# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen
size = [512, 512]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Shape Drawing")
 
#Set needed variables
done = False
clock = pygame.time.Clock()
start = Point(0.0,0.0)
end = Point(0.0,0.0)



#linelist = loadHouse()



CAMERA = [0, 5, 40]
TRANSLATE = [0,0,0]
ROTATE = 180
OBJROT = 0
FOV = 360
NEAR = 0.1
FAR = 1000
LINELIST = []

def buildHouse():
	OBJROT = 0
	TRANSLATE = [0,0,0]
	for i in range(3):
		tempHouse = loadHouse()
		for s in tempHouse:
			s.start.x, s.start.y, s.start.z, homog = toWorld(np.array([[s.start.x],[s.start.y],[s.start.z],[1]]), TRANSLATE, OBJROT)
			s.end.x, s.end.y, s.end.z, homog = toWorld(np.array([[s.end.x],[s.end.y],[s.end.z],[1]]), TRANSLATE, OBJROT)
		for l in tempHouse:
			LINELIST.append(l)
		TRANSLATE[0] += 13
		if TRANSLATE[2] == 0:
			TRANSLATE[2] += 5
		else:
			TRANSLATE[2] *= 3
		OBJROT += 25
	OBJROT = 180
	TRANSLATE = [5, 0, 45]
	for i in range(3):
		tempHouse = loadHouse()
		for s in tempHouse:
			s.start.x, s.start.y, s.start.z, homog = toWorld(np.array([[s.start.x],[s.start.y],[s.start.z],[1]]), TRANSLATE, OBJROT)
			s.end.x, s.end.y, s.end.z, homog = toWorld(np.array([[s.end.x],[s.end.y],[s.end.z],[1]]), TRANSLATE, OBJROT)
		for l in tempHouse:
			LINELIST.append(l)
		TRANSLATE[0] -= 13
		if TRANSLATE[2] == 45:
			TRANSLATE[2] -= 5
		else:
			TRANSLATE[2] *= 0.7
		OBJROT += 25
	OBJROT = 0
	TRANSLATE = [5,0,20]
	CAR = loadCar()
	for s in CAR:
		s.start.x, s.start.y, s.start.z, homog = toWorld(np.array([[s.start.x],[s.start.y],[s.start.z],[1]]), TRANSLATE, OBJROT)
		s.end.x, s.end.y, s.end.z, homog = toWorld(np.array([[s.end.x],[s.end.y],[s.end.z],[1]]), TRANSLATE, OBJROT)
	for l in CAR:
		LINELIST.append(l)
	TRANSLATE[0] += 2
	TRANSLATE[2] += 2
	for i in range(2):
		TIRE = loadTire()
		for s in TIRE:
			s.start.x, s.start.y, s.start.z, homog = toWorld(np.array([[s.start.x],[s.start.y],[s.start.z],[1]]), TRANSLATE, OBJROT)
			s.end.x, s.end.y, s.end.z, homog = toWorld(np.array([[s.end.x],[s.end.y],[s.end.z],[1]]), TRANSLATE, OBJROT)
		for l in TIRE:
			LINELIST.append(l)
		TRANSLATE[0] -= 4
	TRANSLATE[0] += 8
	TRANSLATE[2] -= 4
	for i in range(2):
		TIRE = loadTire()
		for s in TIRE:
			s.start.x, s.start.y, s.start.z, homog = toWorld(np.array([[s.start.x],[s.start.y],[s.start.z],[1]]), TRANSLATE, OBJROT)
			s.end.x, s.end.y, s.end.z, homog = toWorld(np.array([[s.end.x],[s.end.y],[s.end.z],[1]]), TRANSLATE, OBJROT)
		for l in TIRE:
			LINELIST.append(l)
		TRANSLATE[0] -= 4
		

def toWorld(point, trans, rot):
	transMat = np.array([[1, 0, 0, trans[0]],
						[0, 1, 0, trans[1]],
						[0, 0, 1 , trans[2]],
						[0, 0, 0, 1]])
	rotMat = np.array([[np.cos(np.radians(rot)), 0, -np.sin(np.radians(rot)), 0],
						[0, 1, 0, 0],
						[np.sin(np.radians(rot)), 0, np.cos(np.radians(rot)), 0],
						[0, 0, 0, 1]])
	#return np.matmul(transMat, np.matmul(rotMat, point))
	toReturn = np.matmul(transMat, np.matmul(rotMat, point))
	return toReturn[0][0], toReturn[1][0], toReturn[2][0], toReturn[3][0]

def toCamera(point, camPos, rot):
	transMat = np.array([[1,0,0,-camPos[0]],
						[0,1,0,-camPos[1]],
						[0,0,1,-camPos[2]],
						[0,0,0,1]])
	rotMat = np.array([[np.cos(np.radians(rot)), 0, -np.sin(np.radians(rot)), 0],
						[0, 1, 0, 0],
						[np.sin(np.radians(rot)), 0, np.cos(np.radians(rot)), 0],
						[0, 0, 0, 1]])
	return np.matmul(rotMat, np.matmul(transMat, point))   

def toClip(point, fov, near, far):
	zoom = 1/np.tan(fov/2)
	clipMat = np.array([[zoom, 0, 0, 0],
						[0, zoom, 0, 0],
						[0, 0, (far+near)/(far-near), (-2*near*far)/(far-near)],
						[0, 0, 1, 0]])
	return np.matmul(clipMat,point)
	#if clipPoint[0][0] > -clipPoint[3][0] and clipPoint[0][0] < clipPoint[3][0] and clipPoint[1][0] > -clipPoint[3][0] and clipPoint[1][0] < clipPoint[3][0] and clipPoint[2][0] > -clipPoint[3][0] and clipPoint[2][0] < clipPoint[3][0]:
	#	normalPoint = np.array([[clipPoint[0][0]/clipPoint[3][0]],[clipPoint[1][0]/clipPoint[3][0]],[1]])
	#	screenMat = np.array([[size[0]/2,0,size[0]/2],[0,-size[1]/2,size[1]/2],[0,0,1]])
	#	return np.matmul(screenMat,normalPoint)
	#else:
	#	return np.full((4, 4), np.inf)

def toDraw(sPoint, ePoint):
	if (sPoint[2][0] < -sPoint[3][0]) or (ePoint[2][0] < -ePoint[3][0]):
		return np.full((2,2), math.inf),np.full((2,2), math.inf)
	elif (sPoint[0][0] > -sPoint[3][0] and sPoint[0][0] < sPoint[3][0] and sPoint[1][0] > -sPoint[3][0] and sPoint[1][0] < sPoint[3][0] and sPoint[2][0] > -sPoint[3][0] and sPoint[2][0] < sPoint[3][0]) or (ePoint[0][0] > -ePoint[3][0] and ePoint[0][0] < ePoint[3][0] and ePoint[1][0] > -ePoint[3][0] and ePoint[1][0] < ePoint[3][0] and ePoint[2][0] > -ePoint[3][0] and ePoint[2][0] < ePoint[3][0]):
		normalStart = np.array([[sPoint[0][0]/sPoint[3][0]],[sPoint[1][0]/sPoint[3][0]],[1]])
		normalEnd = np.array([[ePoint[0][0]/ePoint[3][0]],[ePoint[1][0]/ePoint[3][0]],[1]])
		screenMat = np.array([[size[0]/2,0,size[0]/2],[0,-size[1]/2,size[1]/2],[0,0,1]])
		return np.matmul(screenMat,normalStart), np.matmul(screenMat,normalEnd)
	else:
		return np.full((2,2), math.inf),np.full((2,2), math.inf)


buildHouse()
#Loop until the user clicks the close button.
while not done:
 
	# This limits the while loop to a max of 100 times per second.
	# Leave this out and we will use all CPU we can.
	clock.tick(100)

	# Clear the screen and set the screen background
	screen.fill(BLACK)

	#Controller Code#
	#####################################################################

	for event in pygame.event.get():
		if event.type == pygame.QUIT: # If user clicked close
			done=True
			
	pressed = pygame.key.get_pressed()

	if pressed[pygame.K_a]:
		CAMERA[2] += np.cos(np.radians(ROTATE - 90))
		CAMERA[0] += np.sin(np.radians(ROTATE - 90))
	if pressed[pygame.K_s]:
		CAMERA[2] -= np.cos(np.radians(ROTATE))
		CAMERA[0] -= np.sin(np.radians(ROTATE))
	if pressed[pygame.K_d]:
		CAMERA[2] += np.cos(np.radians(ROTATE + 90))
		CAMERA[0] += np.sin(np.radians(ROTATE + 90))
	if pressed[pygame.K_f]:
		CAMERA[1] -= 1
	if pressed[pygame.K_q]:
		ROTATE -= 1
	if pressed[pygame.K_w]:
		CAMERA[2] += np.cos(np.radians(ROTATE))
		CAMERA[0] += np.sin(np.radians(ROTATE))
	if pressed[pygame.K_e]:
		ROTATE += 1
	if pressed[pygame.K_r]:
		CAMERA[1] += 1
	if pressed[pygame.K_h]:
		CAMERA = [0,5,40]
		ROTATE = 180

	#Viewer Code#
	#####################################################################

	for s in LINELIST:
		#BOGUS DRAWING PARAMETERS SO YOU CAN SEE THE HOUSE WHEN YOU START UP
		#pygame.draw.line(screen, BLUE, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))
		startP = np.array([[s.start.x],[s.start.y],[s.start.z],[1]])
		#startP = toWorld(np.array([[startP.x],[startP.y],[startP.z],[1]]), TRANSLATE, ROTATE)
		startP = toCamera(startP, CAMERA, ROTATE)
		startP = toClip(startP, FOV, NEAR, FAR)
		endP = np.array([[s.end.x],[s.end.y],[s.end.z],[1]])
		#endP = toWorld(np.array([[endP.x],[endP.y],[endP.z],[1]]), TRANSLATE, ROTATE)
		endP = toCamera(endP, CAMERA, ROTATE)
		endP = toClip(endP, FOV, NEAR, FAR)
		startP, endP = toDraw(startP, endP)
		if startP[0][0] != math.inf or endP[0][0] != math.inf:
			pygame.draw.line(screen, BLUE, (startP[0][0], startP[1][0]), (endP[0][0], endP[1][0]))
	# Go ahead and update the screen with what we've drawn.
	# This MUST happen after all the other drawing commands.
	pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()
