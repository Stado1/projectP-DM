import os
import time
import math
import random
import numpy as np
import matplotlib.pyplot as plt

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
			
			
def readCurrentCoordinates():
	file_name = "currentCoordinates.txt"
	
	with open(file_name, 'r') as file:
		lines = file.readlines()
		return [float(line.strip()) for line in lines]
	
	
	
def main():
	goalCoords = readGoalCoordinates()
	error = 0.55
	
	for gCoord in goalCoords:
		writeCoordinates(gCoord)
		cCoord = []
		#print("c = ", cCoord, ",   g = ", gCoord)
		
		while len(cCoord) < 3:
			cCoord = readCurrentCoordinates()
			print("c = ", cCoord, ",   g = ", gCoord)
				
		
		while ((abs(gCoord[0] - cCoord[0]) > error) or (abs(gCoord[1] - cCoord[1]) > error) or (abs(gCoord[2] - cCoord[2]) > error)):
		
			while len(cCoord) < 3:
				cCoord = readCurrentCoordinates()
				
		
			#time.sleep(0.5)
			
		time.sleep(1.0)
		
	
if __name__ == "__main__":
	main()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
