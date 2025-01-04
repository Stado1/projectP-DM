import os
import time
import math
import random
import numpy as np
#import pybullet as p
import matplotlib.pyplot as plt
#from gym_pybullet_drones.envs.BaseAviary import BaseAviary

# read coordinates from the route.txt file and return them as a list
def readGoalCoordinates():

	file_name = "route.txt"
	coordinates = []

	with open(file_name, 'r') as file:
		for line in file:
			line = line.strip().strip('()')
			if line:
				x, y, z = map(float, line.split(','))
				coordinates.append((x,y,z))
	return coordinates
	
# write coordinates to goalCoordinates.txt
def writeCoordinates(coordinates):
	file_name = "goalCoordinates.txt"
	with open(file_name, 'w') as file:
		for coord in coordinates:
			file.write(f"{coord}\n")
			
# Read the coordinates of where the robot currently is from currentCoordinates.txt		
def readCurrentCoordinates():
	file_name = "currentCoordinates.txt"
	
	with open(file_name, 'r') as file:
		lines = file.readlines()
		return [float(line.strip()) for line in lines]
		
		
	
# calculate the distance between 2 points in a 3d space	
def calculateDistance(gCoord, cCoord):
	return ((gCoord[0] - cCoord[0]) * (gCoord[0] - cCoord[0]) +
			(gCoord[1] - cCoord[1]) * (gCoord[1] - cCoord[1]) +
			(gCoord[2] - cCoord[2]) * (gCoord[2] - cCoord[2])) ** 0.5
			
					
	
	
def main():
	goalCoords = readGoalCoordinates() 
	error = 0.15 # this is the maximum allowable distance between the drone position and the waypoint position
	
	
	# loop trough all the waypoints
	for gCoord in goalCoords:
		writeCoordinates(gCoord)
		cCoord = []
		
		# sometimes the coordinates are not read correctly so this ensures that they will be read again until they are read correctly
		while len(cCoord) < 3:
			cCoord = readCurrentCoordinates()
			#print("c = ", cCoord, ",   g = ", gCoord)
				
		distance = calculateDistance(gCoord, cCoord)
		print("c = ", cCoord, ",   g = ", gCoord)
		print(distance)
		
		# keep looping until the drone is close enough to the target waypoint.
		while (distance > error):
		
			cCoord = readCurrentCoordinates()
			while len(cCoord) < 3:
				cCoord = readCurrentCoordinates()
			
			distance = calculateDistance(gCoord, cCoord)
			print("c = ", cCoord, ",   g = ", gCoord)
			print(distance)
			time.sleep(0.1)
		
		time.sleep(0.1)
		
		
		
		
	
if __name__ == "__main__":
	main()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
