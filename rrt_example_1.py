from planner.rrt_3d_planner import rrt_planning
from plotting.plot_rrt_3d import plot_rrt_3d
from plotting.plot_rrt_3d_interactive import plot_rrt_3d_interactive

if __name__ == "__main__":
    # Define parameters
    start_coord = (0.0, 0.0, 5.0)
    end_coord = (5.0, 0.0, 5.0)

    min_x, max_x = -2.0, 7.0
    min_y, max_y = -3.0, 3.0
    min_z, max_z = 2.0, 8.0

    obstacles = [
        (2.0, 3.0, -0.5, 0.5, 4.5, 5.5)
    ]

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
        print("Path found:")
        #for waypoint in path:
            #print(waypoint)
            
        # deletes all the old waypoints from the file and then 
        # adds all the new waypoints to the "route.txt" file
        with open("route.txt", "w") as file:
            for waypoint in path:
                file.write(f"{waypoint}\n")
        
        # Plot with matplotlib
        plot_rrt_3d(path, start_coord, end_coord, obstacles,
                    min_x, max_x, min_y, max_y, min_z, max_z)

        # Plot interactively with plotly
        plot_rrt_3d_interactive(path, start_coord, end_coord, obstacles,
                                min_x, max_x, min_y, max_y, min_z, max_z)
    else:
        print("No path found after maximum iterations.")
