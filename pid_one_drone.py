"""Script demonstrating the joint use of simulation and control.

The simulation is run by a `CtrlAviary` environment.
The control is given by the PID implementation in `DSLPIDControl`.

Example
-------
In a terminal, run as:

    $ python3 pid_one_drone.py

Notes
-----
The drones move, at different altitudes, along cicular trajectories 
in the X-Y plane, around point (0, -.3).

"""
import os
import time
import argparse
from datetime import datetime
import pdb
import math
import random
import numpy as np
import pybullet as p
import matplotlib.pyplot as plt

from gym_pybullet_drones.utils.enums import DroneModel, Physics
from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
from gym_pybullet_drones.utils.Logger import Logger
from gym_pybullet_drones.utils.utils import sync, str2bool

DEFAULT_DRONES = DroneModel("cf2x")
DEFAULT_NUM_DRONES = 1
DEFAULT_PHYSICS = Physics("pyb")
DEFAULT_GUI = True
DEFAULT_RECORD_VISION = False
DEFAULT_PLOT = True
DEFAULT_USER_DEBUG_GUI = True
DEFAULT_OBSTACLES = True
DEFAULT_SIMULATION_FREQ_HZ = 240
DEFAULT_CONTROL_FREQ_HZ = 48
DEFAULT_DURATION_SEC = 600
DEFAULT_OUTPUT_FOLDER = 'results'
DEFAULT_COLAB = False

def run(
        drone=DEFAULT_DRONES,
        num_drones=DEFAULT_NUM_DRONES,
        physics=DEFAULT_PHYSICS,
        gui=DEFAULT_GUI,
        record_video=DEFAULT_RECORD_VISION,
        plot=DEFAULT_PLOT,
        user_debug_gui=DEFAULT_USER_DEBUG_GUI,
        obstacles=DEFAULT_OBSTACLES,
        simulation_freq_hz=DEFAULT_SIMULATION_FREQ_HZ,
        control_freq_hz=DEFAULT_CONTROL_FREQ_HZ,
        duration_sec=DEFAULT_DURATION_SEC,
        output_folder=DEFAULT_OUTPUT_FOLDER,
        colab=DEFAULT_COLAB
        ):
    #### Initialize the simulation #############################
    H = .1
    H_STEP = .05
    R = .3
    INIT_XYZS = np.array([[0, 0, 1]]) # starting coordinates
    INIT_RPYS = np.array([[0, 0,  0]]) # starting orientation
	

    #### Create trajectory ######################
    # this creates the initial trajectory to the first coordinate,
    # later in the code the coordinates in TARGET_POS are refreshed 
    # by reading from the txt file 
    
    PERIOD = 10
    NUM_WP = control_freq_hz*PERIOD
    TARGET_POS = np.zeros((NUM_WP,3))
    
    for i in range(NUM_WP):
    	with open("goalCoordinates.txt", "r") as file:
    		variables = [float(line.strip()) for line in file]
    	TARGET_POS[i, :] = variables[0], variables[1], variables[2]
    	
    wp_counters = np.array([int((i*NUM_WP/6)%NUM_WP) for i in range(num_drones)])




    #### Create the environment ################################
    env = CtrlAviary(drone_model=drone,
                        num_drones=num_drones,
                        initial_xyzs=INIT_XYZS,
                        initial_rpys=INIT_RPYS,
                        physics=physics,
                        neighbourhood_radius=10,
                        pyb_freq=simulation_freq_hz,
                        ctrl_freq=control_freq_hz,
                        gui=gui,
                        record=record_video,
                        obstacles=obstacles,
                        user_debug_gui=user_debug_gui
                        )

    #### Obtain the PyBullet Client ID from the environment ####
    PYB_CLIENT = env.getPyBulletClient()

    #### Initialize the logger #################################
    logger = Logger(logging_freq_hz=control_freq_hz,
                    num_drones=num_drones,
                    output_folder=output_folder,
                    colab=colab
                    )

    #### Initialize the controllers ############################
    if drone in [DroneModel.CF2X, DroneModel.CF2P]:
        ctrl = [DSLPIDControl(drone_model=drone) for i in range(num_drones)]


    #### Load all the obstacles ################################
    
    # this is a function to load coordinates from text files
    def parseCoordinates(filePath):
        coords = []
        with open(filePath, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("(") and line.endswith(")"):
                    coord = line[1:-1].split(",")
                    coords.append(tuple(map(float, coord)))
        return coords
        
    # load the locations for the obstalces from txt file
    coordinatesObstacles = parseCoordinates("obsLocationRandom.txt")
    
    # loop trough the coordinates and load an obtsacle at each point
    for coord in coordinatesObstacles:
        x, y, z = coord
        obstacle = p.loadURDF("cube.urdf",
                   [x, y, z],
                   useFixedBase=True,
                   globalScaling=0.95,
                   )
        p.changeVisualShape(obstacle, -1, rgbaColor=[1,0,0,0.3])
        p.setCollisionFilterGroupMask(obstacle, -1, collisionFilterGroup=1, collisionFilterMask=2)


    #### Load visuals at waypoints #############################
    
    # store all waypoints in a variable
    coordinatesWaypoints = parseCoordinates("route.txt")
    
    #loop trough all the waypoints and place visuals at each point
    for i, coord in enumerate(coordinatesWaypoints):
        x, y, z = coord
        if i == len(coordinatesWaypoints) - 1: # visual for the final waypoint
            endPoint = p.loadURDF("cube.urdf", [x, y, z], useFixedBase=True, globalScaling=0.1)
            p.setCollisionFilterGroupMask(endPoint, -1, collisionFilterGroup=0, collisionFilterMask=0)
            p.changeVisualShape(endPoint, -1, rgbaColor=[0,1,0,0.9])
        else: # visuals for all other waypoints
            waypointCube = p.loadURDF("cube.urdf", [x, y, z], useFixedBase=True, globalScaling=0.05)
            p.setCollisionFilterGroupMask(waypointCube, -1, collisionFilterGroup=0, collisionFilterMask=0)
            p.changeVisualShape(waypointCube, -1, rgbaColor=[1,1,0,0.5])
            

    print("All obstacles and waypoints are loaded.")
    #### Run the simulation ####################################
    action = np.zeros((num_drones,4))
    START = time.time()
    for i in range(0, int(duration_sec*env.CTRL_FREQ)):
        
        # Here are the coordinates read from the txt file
        for i in range(NUM_WP):
    	    with open("goalCoordinates.txt", "r") as file:
    	        newVariables = [float(line.strip()) for line in file if line.strip()]
    	    		
    	    if newVariables:
    	    	variables = newVariables
    	    	
    	    TARGET_POS[i, :] = variables[0], variables[1], variables[2]

        #### Make it rain rubber ducks #############################
        # if i/env.SIM_FREQ>5 and i%10==0 and i/env.SIM_FREQ<10: p.loadURDF("duck_vhacd.urdf", [0+random.gauss(0, 0.3),-0.5+random.gauss(0, 0.3),3], p.getQuaternionFromEuler([random.randint(0,360),random.randint(0,360),random.randint(0,360)]), physicsClientId=PYB_CLIENT)

        #### Step the simulation ###################################
        obs, reward, terminated, truncated, info = env.step(action)

        #### Compute control for the current way point #############
        for j in range(num_drones):
            action[j, :], _, _ = ctrl[j].computeControlFromState(control_timestep=env.CTRL_TIMESTEP,
                                                                    state=obs[j],
                                                                    target_pos=np.hstack([TARGET_POS[wp_counters[j], 0:3]]),
                                                                    # target_pos=INIT_XYZS[j, :] + TARGET_POS[wp_counters[j], :],
                                                                    target_rpy=INIT_RPYS[j, :]
                                                                    )

        #### Go to the next way point and loop #####################
        for j in range(num_drones):
            wp_counters[j] = wp_counters[j] + 1 if wp_counters[j] < (NUM_WP-1) else 0

        #### Log the simulation ####################################
        for j in range(num_drones):
            logger.log(drone=j,
                       timestamp=i/env.CTRL_FREQ,
                       state=obs[j],
                       control=np.hstack([TARGET_POS[wp_counters[j], 0:2], INIT_XYZS[j, 2], INIT_RPYS[j, :], np.zeros(6)])
                       # control=np.hstack([INIT_XYZS[j, :]+TARGET_POS[wp_counters[j], :], INIT_RPYS[j, :], np.zeros(6)])
                       )

        #### Printout ##############################################
        #aap = env.render()
        
        ## Write info to currentCoordinates.txt ####################
        #print(f"x = {env.pos[0, 0]:.2f}, y = {env.pos[0, 1]:.2f}, z = {env.pos[0, 2]:.2f}")
        
        with open("currentCoordinates.txt", "w") as file:
        	file.write(f"{env.pos[0, 0]:.2f}\n")
        	file.write(f"{env.pos[0, 1]:.2f}\n")
        	file.write(f"{env.pos[0, 2]:.2f}\n")

        #### Sync the simulation ###################################
        if gui:
            sync(i, START, env.CTRL_TIMESTEP)

    #### Close the environment #################################
    env.close()

    #### Save the simulation results ###########################
    logger.save()
    logger.save_as_csv("pid") # Optional CSV save

    #### Plot the simulation results ###########################
    if plot:
        logger.plot()

if __name__ == "__main__":
    #### Define and parse (optional) arguments for the script ##
    parser = argparse.ArgumentParser(description='Helix flight script using CtrlAviary and DSLPIDControl')
    parser.add_argument('--drone',              default=DEFAULT_DRONES,     type=DroneModel,    help='Drone model (default: CF2X)', metavar='', choices=DroneModel)
    parser.add_argument('--num_drones',         default=DEFAULT_NUM_DRONES,          type=int,           help='Number of drones (default: 3)', metavar='')
    parser.add_argument('--physics',            default=DEFAULT_PHYSICS,      type=Physics,       help='Physics updates (default: PYB)', metavar='', choices=Physics)
    parser.add_argument('--gui',                default=DEFAULT_GUI,       type=str2bool,      help='Whether to use PyBullet GUI (default: True)', metavar='')
    parser.add_argument('--record_video',       default=DEFAULT_RECORD_VISION,      type=str2bool,      help='Whether to record a video (default: False)', metavar='')
    parser.add_argument('--plot',               default=DEFAULT_PLOT,       type=str2bool,      help='Whether to plot the simulation results (default: True)', metavar='')
    parser.add_argument('--user_debug_gui',     default=DEFAULT_USER_DEBUG_GUI,      type=str2bool,      help='Whether to add debug lines and parameters to the GUI (default: False)', metavar='')
    parser.add_argument('--obstacles',          default=DEFAULT_OBSTACLES,       type=str2bool,      help='Whether to add obstacles to the environment (default: True)', metavar='')
    parser.add_argument('--simulation_freq_hz', default=DEFAULT_SIMULATION_FREQ_HZ,        type=int,           help='Simulation frequency in Hz (default: 240)', metavar='')
    parser.add_argument('--control_freq_hz',    default=DEFAULT_CONTROL_FREQ_HZ,         type=int,           help='Control frequency in Hz (default: 48)', metavar='')
    parser.add_argument('--duration_sec',       default=DEFAULT_DURATION_SEC,         type=int,           help='Duration of the simulation in seconds (default: 5)', metavar='')
    parser.add_argument('--output_folder',     default=DEFAULT_OUTPUT_FOLDER, type=str,           help='Folder where to save logs (default: "results")', metavar='')
    parser.add_argument('--colab',              default=DEFAULT_COLAB, type=bool,           help='Whether example is being run by a notebook (default: "False")', metavar='')
    ARGS = parser.parse_args()

    run(**vars(ARGS))
