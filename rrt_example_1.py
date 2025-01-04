from planner.rrt_3d_planner import rrt_planning
from plotting.plot_rrt_3d import plot_rrt_3d
from plotting.plot_rrt_3d_interactive import plot_rrt_3d_interactive


 # this is a function to load coordinates from text files
def readAndConvertCoordinates(fileName):
    obs = []
    with open(fileName, 'r') as file:
        for line in file:
            line = line.strip().strip('()')
            x, y, z = map(float, line.split(","))
            obs.append((x-0.5, x+0.5, y-0.5, y+0.5, z-0.5, z+0.5))
    return obs


# Define parameters
start_coord = (0.0, 0.0, 1.0)
end_coord = (6.0, 6.0, 7.0)

min_x, max_x = -1.0, 7.0
min_y, max_y = -1.0, 7.0
min_z, max_z = 0.5, 8.0

# load the locations for the obstalces from txt file
obstacles = readAndConvertCoordinates("obsLocationRandom.txt")

# obstacles = [
#    (2.0, 3.0, -0.5, 0.5, 4.5, 5.5),
#    (5.0, 4.0, -0.5, 0.5, 4.5, 3.5),
#     (2.0, 3.0, 2.0, 1.0, 4.5, 5.5),
#     (2.0, 3.0, -0.5, 0.5, 7.0, 6.0),
#     (2.0, 3.0, -2.0, -1.0, 4.5, 5.5),
#  ]

# Run RRT
path = rrt_planning(
        start=start_coord,
        goal=end_coord,
        obstacles=obstacles,
        min_x=min_x, max_x=max_x,
        min_y=min_y, max_y=max_y,
        min_z=min_z, max_z=max_z,
        expand_dist=0.1,
        goal_sample_rate=0.05,
        max_iter=10000,
        goal_tolerance=0.05
    )

if path is not None:
    print("Path found")
    #for waypoint in path:
       #print(waypoint)
            
    # deletes all the old waypoints from the file and then 
    # adds all the new waypoints to the "route.txt" file
    with open("route.txt", "w") as file:
        for waypoint in path:
            file.write(f"{waypoint}\n")
        
    print("Click plot away to continue")
    # Plot with matplotlib
    plot_rrt_3d(path, start_coord, end_coord, obstacles,
                    min_x, max_x, min_y, max_y, min_z, max_z)

    # Plot interactively with plotly
    #plot_rrt_3d_interactive(path, start_coord, end_coord, obstacles,
    #                            min_x, max_x, min_y, max_y, min_z, max_z)
else:
    print("No path found after maximum iterations.")
