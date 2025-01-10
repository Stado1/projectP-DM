# projectP-DM

## How to use 

1. Install 'projectP-DM' in 'gym-pybullet-drones/gym-pybullet-drones/examples/ .

2. Open a terminal and go to the 'projectP-DM' folder. Activate the drones environment by typing: "conda activate drones" in the terminal.

3. Run the 'runRandomTest.sh' bash script. This script will put the obstacles at random positions, create a path trought the obstacles and then open the simulation environment. Running this script will first open a plot with the route, when you click this plot away then the simulation will start.

4. Wait until everything is loaded in the simulation. (So each red obstacle, each yellow waypoint dot and the green finish dot. All in that order.)

5. Open a new terminal and go to the projectP-DM folder. Now run the drone control code by typing: "python3 droneController.py"

The drone should now follow the route that was created by the rrt\_example\_1.py code.

Note: sometimes the route that is created by "rrt\_example\_1.py" will be invalid and the drone will crash, just repeat steps 3, 4 and 5 to create a new route.


### Camera problem
I had a problem with adjusting the camera in the simulation where i can only zoom in and out but not move the position of the camera.
If you also have this problem you can open the file: 'gym-pybullet-drones/gym-pybullet-drones/envs/BaseAviary.py'. On lines 153 till 158, at p.resetDebugVisualizerCamera you can change the coordinates of the camera. If you set the distance=1, yaw=-45, pitch=35 and the coordinates to (-1, -1, 0) then you can follow the drone by just zooming in and out.

### Simulation running slowly
If the simulation is running very slow and lagging a lot then go to the "droneController.py" file and uncomment the lines 79 and 81. (the lines that contain "time.sleep(0.1)")


## How it works
The 'runRandomTest.sh' script will first reset the current values for "goalCoordinates.txt".

Then it will run the file "generateRandomObstacles.py", which will place obstacles in random locations in the environment

After that it will run the file "rrt\_example\_1.py" which creates a path that consists of waypoints and stores all these waypoints into "route.txt".

Then the script will start "pid\_one\_drone.py" which will open the environment and load in all the obstacles, waypoints and the final point. This code will also constantly write the current position of the drone to "currentCoordinate.txt". 

The "droneController.py" will look at the next waypoint and send those coordinates to "goalCoordinates.txt", these coordinates will be read by "pid\_one\_drone.py" and the drone will then fly to those coordinates. Then "droneController.py" will constantly check if the drone has reached that waypoint by looking at the "currentCoordinates.txt" and comparing them to the coordinates of the current waypoint. Once the waypoint is reached the code will send the coordinates for the next waypoint and the cycle repeats. 











