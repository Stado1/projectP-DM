# projectP-DM

## How to use pid\_one\_drone.py

1. activate the drones anvironment by typing: "conda activate drones" in the terminal.

2. run the python file by typing: "python3 pid\_one\_drone.py" in the terminal

3. then in a text editor open the text file: "goalCoordinates.txt"

4. in this text file the are 3 numbers: on line 1 it is the x coordinate, on line 2 it is the y coordinate and on line 3 it is the z coordinate.
If you change the value of any of these coordinates and then save the file the drone should fly to that position in the simulation.
If you type values that are too far away from the current coordinates the drone will lose balance and crash, so try to make it not fly more than 1.0 meters at a time.

# How it works

The drone reads the coordinates from the goalCoordinates.txt file. It will simultaniously write the current coordinates to the currentCoordinates.txt file, this file needs to be closed and reopend if you want to see the most current position.
