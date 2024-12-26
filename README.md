# projectP-DM

## How to use 

1. Activate the drones anvironment by typing: "conda activate drones" in the terminal.

2. Reset the current position by changing the coordinates in "goalCoordinates.txt" to 0.0, 0.0, 1.0.

3. Create a path for the drone to follow by running in a terminal: "python3 rrt\_example\_1.py". (This is optional because sometimes the route that this file will create is not possible because the drone will fly too close too the ground and crash. The route that is currently in route.txt is a route that the drone can follow without crashing.)

4. Start the enviroment by typing: "python3 pid\_one\_drone.py" in the terminal.

5. Open a new terminal and go to the projectP-DM folder. Now run the drone control code by typing: "python3 droneController.py"

The drone should now follow the route that was created by the rrt\_example\_1.py code.



## How it works
The file "rrt\_example\_1.py" creates a path that consists of waypoints and stores all these waypoints into "route.txt".\\
Then starting "pid\_one\_drone.py" will open the environment. This code will also constantly write the current position of the drone to "currentCoordinate.txt". \\
The "droneController.py" will look at the next waypoint and send those coordinates to "goalCoordinates.txt", these coordinates will be read by "pid\_one\_drone.py" and the drone will then fly to those coordinates. Then "droneController.py" will constantly check if the drone has reached that waypoint by looking at the "currentCoordinates.txt" and comparing them to the coordinates of the waypoint. Once the waypoint is reached the code will send the coordinates for the next waypoint and the cycle repeats. 



## What needs to be done

- The rrt\_example\_1.py code can sometimes create a route that goes too close to the ground. This code needs to be adjusted such that there is a minumum value for z-coordinate where every waypoint needs to be above.

- Find a way to adjust the speed of the drone.

- Create visualisation in the environment of where each waypoint is.

- Find a way to randomly generate locations for obstacles and then load those abstacles into the environment and into the route planner.

- Find a way to change the position of the camera in the environment.

- Find a way to reduce the allowable error in "droneController.py".







