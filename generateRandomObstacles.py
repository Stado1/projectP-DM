import random

coordinates = []


# define the amount of obstacles in the environment
numOfObstacles = 15

# generate locations for each obstacle
for _ in range(numOfObstacles):
    x = random.uniform(0,6)
    y = random.uniform(0,6)
    z = random.uniform(2,6)
    coordinates.append((x, y, z))
    
with open("obsLocationRandom.txt", 'w') as file:
     for coord in coordinates:
         file.write(f"({coord[0]:.2f}, {coord[1]:.2f}, {coord[2]:.2f})\n")


