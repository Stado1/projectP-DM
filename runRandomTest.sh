#!/bin/bash

# Reset starting coordinates for "goalCoordinates.txt"
echo "reset coordinates"
cat <<EOL > goalCoordinates.txt
0.0
0.0
1.0
EOL

# Generate positions of obstacles
echo "Placing obstacles on random positions"
python3 generateRandomObstacles.py
echo "Succesfully placed obstacles"


# Generate path
echo "Generating a path trough the obstacles, this may take a while...."
python3 rrt_example_1.py 


# Start "PID_one_drone.py" to start the environment
echo "Starting the environment"
echo "Wait until the path is completely loaded and then in a new terminal run the python code 'droneController.py'"
python3 pid_one_drone.py
 
 
