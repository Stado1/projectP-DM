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
The simulation works by first generating random locations for the obstacles, this is done by "generateRandomObstacle.py". These coordinates are written to the text file "obsLocationRandom.txt". The obstacle coordinates are then read by "rrt\_example\_1.py" and this python file will then create a path around those obstacles. This is done by creating waypoints close to each other and connecting these waypoints to form a path. These waypoints are stored in "route.txt". 
The "pid\_one\_drone.py" is then started which will start the environment and read the obstacle locations from "obsLocationRandom.txt" and place the obstacles in the environment, which are red see trough cubes. It will then read the waypoint locations from "route.txt" and place visualisations for each waypoint, which are small yellow cubes with the last waypoint being the finish which is a small green cube. It will also load in the drone.
The python file "droneController.py" will iterate trough these waypoints. It will take the first waypoint and write them to "goalCoordinates.txt" this file is read by the python file "pid\_one\_drone.py" which will move the drone to that waypoint. Simultaneously, "pid\_one\_drone.py" is constantly writing the current location of the drone to "currentCoordinates.txt". This text file is also constantly read by "droneController.py" and when the drone is close enough to the waypoint, "droneController.py" will change the coordinates in "goalCoordinates.txt" to the coordinates of the next waypioints. These steps keep repeating until the drone reaches the final waypoint which is the end point.

A chart of this sumulation: ![alt text]([http://url/to/img.png](https://github.com/Stado1/projectP-DM/blob/main/SimulationSetup.png)











