import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from tqdm import tqdm

# ----------------------------
#  Node class and basic utils
# ----------------------------
class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.parent = None
        self.cost = 0.0  # Used only by RRT* to store cost from start

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def steer(from_node, to_point, expand_dist):
    """
    Steer from `from_node` towards `to_point` by `expand_dist`.
    """
    dx = to_point[0] - from_node.x
    dy = to_point[1] - from_node.y
    dz = to_point[2] - from_node.z
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
    if dist < 1e-9:  # Avoid division by zero if points are extremely close
        return Node(to_point[0], to_point[1], to_point[2])
    new_x = from_node.x + expand_dist * dx / dist
    new_y = from_node.y + expand_dist * dy / dist
    new_z = from_node.z + expand_dist * dz / dist
    return Node(new_x, new_y, new_z)

def check_collision(node_from, node_to, obstacles):
    """
    Check if the line segment from node_from to node_to intersects any obstacles.
    Obstacles are axis-aligned 3D boxes defined as (x_min, x_max, y_min, y_max, z_min, z_max).
    """
    seg_dist = distance((node_from.x, node_from.y, node_from.z), 
                        (node_to.x, node_to.y, node_to.z))
    # Step size in collision checking
    step_size = 0.5  
    steps = int(seg_dist / step_size) + 1

    for i in range(steps):
        t = i / float(steps)
        x = node_from.x + t * (node_to.x - node_from.x)
        y = node_from.y + t * (node_to.y - node_from.y)
        z = node_from.z + t * (node_to.z - node_from.z)
        
        # Check each obstacle
        for (ox_min, ox_max, oy_min, oy_max, oz_min, oz_max) in obstacles:
            if (ox_min <= x <= ox_max) and (oy_min <= y <= oy_max) and (oz_min <= z <= oz_max):
                return False
    return True

def get_nearest_node_index(node_list, rnd_point):
    distances = [(node.x - rnd_point[0])**2 + (node.y - rnd_point[1])**2 + (node.z - rnd_point[2])**2
                 for node in node_list]
    min_index = distances.index(min(distances))
    return min_index

def generate_random_point(min_x, max_x, min_y, max_y, min_z, max_z, goal_sample_rate, goal):
    """
    With probability goal_sample_rate, return the goal. Otherwise, random point.
    """
    if random.random() < goal_sample_rate:
        return (goal[0], goal[1], goal[2])
    else:
        rx = random.uniform(min_x, max_x)
        ry = random.uniform(min_y, max_y)
        rz = random.uniform(min_z, max_z)
        return (rx, ry, rz)

def backtrace_path(goal_node):
    """
    Return path from start to goal by backtracking parent pointers of the goal_node.
    """
    path = []
    node = goal_node
    while node is not None:
        path.append((node.x, node.y, node.z))
        node = node.parent
    path.reverse()
    return path

# ----------------
#   RRT
# ----------------
def rrt_planning(start, goal, obstacles, 
                 min_x, max_x, min_y, max_y, min_z, max_z,
                 expand_dist=1.0, goal_sample_rate=0.05, max_iter=1000, goal_tolerance=1.0):
    """
    Basic RRT in 3D.
    """
    start_node = Node(start[0], start[1], start[2])
    goal_node = Node(goal[0], goal[1], goal[2])
    node_list = [start_node]

    for _ in range(max_iter):
        rnd_point = generate_random_point(
            min_x, max_x, min_y, max_y, min_z, max_z, goal_sample_rate, goal
        )
        nearest_index = get_nearest_node_index(node_list, rnd_point)
        nearest_node = node_list[nearest_index]

        new_node = steer(nearest_node, rnd_point, expand_dist)

        if check_collision(nearest_node, new_node, obstacles):
            new_node.parent = nearest_node
            node_list.append(new_node)

            # Check if within tolerance
            if distance((new_node.x, new_node.y, new_node.z),
                        (goal_node.x, goal_node.y, goal_node.z)) < goal_tolerance:
                goal_node.parent = new_node
                return backtrace_path(goal_node)

    return None

# ----------------
#   RRT*
# ----------------
def rrt_star_planning(
    start, goal, obstacles, 
    min_x, max_x, min_y, max_y, min_z, max_z,
    expand_dist=1.0, goal_sample_rate=0.05, max_iter=1000, goal_tolerance=1.0,
    max_radius=2.0):
    """
    RRT* in 3D.
    """
    start_node = Node(start[0], start[1], start[2])
    goal_node = Node(goal[0], goal[1], goal[2])
    start_node.cost = 0.0
    node_list = [start_node]

    for _ in range(max_iter):
        rnd_point = generate_random_point(
            min_x, max_x, min_y, max_y, min_z, max_z, goal_sample_rate, goal
        )

        # 1) Find nearest node
        nearest_index = get_nearest_node_index(node_list, rnd_point)
        nearest_node = node_list[nearest_index]

        # 2) Steer
        new_node = steer(nearest_node, rnd_point, expand_dist)

        # 3) Check collision from nearest_node to new_node
        if not check_collision(nearest_node, new_node, obstacles):
            continue

        # 4) Find nearby nodes within a radius
        #    A common formula: r = gamma * (log(n)/n)^(1/d), but we can keep it simpler.
        #    Here we combine that with max_radius as an upper bound.
        n = len(node_list)
        d = 3.0  # 3D
        gamma = 1.0  # Some constant
        radius = min(max_radius, gamma * (math.log(n) / n)**(1.0/d) * expand_dist + expand_dist)

        nearby_nodes = []
        for node in node_list:
            if distance((node.x, node.y, node.z), (new_node.x, new_node.y, new_node.z)) < radius:
                nearby_nodes.append(node)

        # 5) Choose the best parent = minimal cost
        best_node = nearest_node
        best_cost = nearest_node.cost + distance(
            (nearest_node.x, nearest_node.y, nearest_node.z),
            (new_node.x, new_node.y, new_node.z)
        )

        for near_node in nearby_nodes:
            # Check if collision-free from near_node to new_node
            if check_collision(near_node, new_node, obstacles):
                cost = near_node.cost + distance(
                    (near_node.x, near_node.y, near_node.z),
                    (new_node.x, new_node.y, new_node.z)
                )
                if cost < best_cost:
                    best_cost = cost
                    best_node = near_node

        # Attach new_node to best_node
        new_node.parent = best_node
        new_node.cost = best_cost
        node_list.append(new_node)

        # 6) Rewire: check if we can improve cost of nearby_nodes by going through new_node
        for near_node in nearby_nodes:
            if near_node == best_node:
                continue
            new_cost = new_node.cost + distance(
                (new_node.x, new_node.y, new_node.z),
                (near_node.x, near_node.y, near_node.z)
            )
            # If cheaper and collision-free, then rewire
            if new_cost < near_node.cost:
                if check_collision(new_node, near_node, obstacles):
                    near_node.parent = new_node
                    near_node.cost = new_cost

        # 7) Check goal tolerance
        if distance((new_node.x, new_node.y, new_node.z), (goal_node.x, goal_node.y, goal_node.z)) < goal_tolerance:
            goal_node.parent = new_node
            goal_node.cost = new_node.cost
            return backtrace_path(goal_node)

    return None

# -------------------------------------------------------
#   Plotting and Comparison
# -------------------------------------------------------
def plot_rrt_3d(path, start, goal, obstacles,
                min_x, max_x, min_y, max_y, min_z, max_z,
                title='3D RRT Path Planning', color='blue', label_path='Path'):
    """
    Plots the path in a 3D space with obstacles. 
    This can be reused for either RRT or RRT*.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the start and goal points
    ax.scatter(*start, color='green', s=100, label='Start')
    ax.scatter(*goal, color='red', s=100, label='Goal')

    # Plot obstacles as cubes
    for obstacle in obstacles:
        x_min, x_max, y_min, y_max, z_min, z_max = obstacle
        x_size = x_max - x_min
        y_size = y_max - y_min
        z_size = z_max - z_min
        ax.bar3d(x_min, y_min, z_min, x_size, y_size, z_size, color='gray', alpha=0.5)

    # Plot the path
    if path:
        path_np = np.array(path)
        ax.plot(path_np[:, 0], path_np[:, 1], path_np[:, 2], color=color, linewidth=2, label=label_path)
        ax.scatter(path_np[:, 0], path_np[:, 1], path_np[:, 2], color=color, s=10)

    # Set axes limits
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_zlim(min_z, max_z)

    # Set labels
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title(title)
    ax.legend()
    plt.show()

def plot_comparison_3d(rrt_path, rrt_star_path, start, goal, obstacles,
                       min_x, max_x, min_y, max_y, min_z, max_z):
    """
    Plots both RRT and RRT* paths on the same 3D figure for comparison.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the start and goal points
    ax.scatter(*start, color='green', s=100, label='Start')
    ax.scatter(*goal, color='red', s=100, label='Goal')

    # Plot obstacles as cubes
    for obstacle in obstacles:
        x_min, x_max, y_min, y_max, z_min, z_max = obstacle
        x_size = x_max - x_min
        y_size = y_max - y_min
        z_size = z_max - z_min
        ax.bar3d(x_min, y_min, z_min, x_size, y_size, z_size, color='gray', alpha=0.5)

    # RRT path
    if rrt_path:
        rrt_path_np = np.array(rrt_path)
        ax.plot(rrt_path_np[:, 0], rrt_path_np[:, 1], rrt_path_np[:, 2],
                color='blue', linewidth=2, label='RRT Path')
        ax.scatter(rrt_path_np[:, 0], rrt_path_np[:, 1], rrt_path_np[:, 2], color='blue', s=10)

    # RRT* path
    if rrt_star_path:
        rrt_star_path_np = np.array(rrt_star_path)
        ax.plot(rrt_star_path_np[:, 0], rrt_star_path_np[:, 1], rrt_star_path_np[:, 2],
                color='orange', linewidth=2, label='RRT* Path')
        ax.scatter(rrt_star_path_np[:, 0], rrt_star_path_np[:, 1], rrt_star_path_np[:, 2],
                   color='orange', s=10)

    # Set axes limits
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_zlim(min_z, max_z)

    # Set labels
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('Comparison: RRT vs RRT*')
    ax.legend()
    plt.show()

def compute_path_length(path):
    """
    Compute the total Euclidean length of the path (list of (x,y,z) points).
    """
    if not path or len(path) < 2:
        return 0.0
    length = 0.0
    for i in range(len(path) - 1):
        length += distance(path[i], path[i+1])
    return length

# --------------------
#   Usage
# --------------------
if __name__ == "__main__":
    # Define parameters
    start_coord = (0.0, 0.0, 0.0)
    end_coord = (10.0, 10.0, 10.0)

    min_x, max_x = -5.0, 15.0
    min_y, max_y = -5.0, 15.0
    min_z, max_z = -5.0, 15.0

    obstacles = [
    (2.0, 3.5, 2.0, 3.5, 2.0, 3.5),   # Obstacle 1
    (6.0, 7.5, 6.0, 7.5, 6.0, 7.5),   # Obstacle 2
    (4.0, 6.0, 4.0, 6.0, 4.0, 6.0),   # Obstacle 3
    (8.0, 10.0, 2.0, 4.0, 2.0, 4.0),  # Obstacle 4
    (3.0, 4.0, 7.0, 8.0, 5.0, 6.0),   # Obstacle 5
    (5.5, 6.5, 5.5, 6.5, 1.0, 3.0),   # Obstacle 6
    (1.0, 2.0, 7.0, 9.0, 3.0, 5.0),   # Obstacle 7
    (7.5, 8.5, 1.0, 2.0, 6.0, 8.0),   # Obstacle 8
    (3.5, 5.0, 3.5, 5.0, 7.0, 8.5),   # Obstacle 9
    (9.0, 10.0, 8.0, 9.5, 4.0, 5.5),  # Obstacle 10
    (1.5, 3.0, 4.0, 6.0, 1.5, 3.0),   # Obstacle 11
    (6.0, 7.5, 2.0, 3.5, 7.0, 8.5),   # Obstacle 12
    (8.0, 9.5, 5.0, 6.5, 1.0, 2.5),   # Obstacle 13
    (4.5, 6.0, 1.5, 3.0, 6.0, 7.5),   # Obstacle 14
    (2.5, 4.0, 7.0, 8.5, 4.0, 5.5),   # Obstacle 15
    (6.0, 7.0, 7.0, 8.0, 6.0, 7.0),   # Obstacle 16
    (3.0, 4.5, 5.0, 6.5, 3.0, 4.5),   # Obstacle 17
    (9.0, 10.0, 2.0, 3.5, 7.0, 8.5),  # Obstacle 18
    (1.5, 3.0, 8.0, 9.5, 2.5, 4.0),   # Obstacle 19
    (5.0, 6.5, 4.0, 5.5, 1.5, 3.0),   # Obstacle 20
    (6.5, 8.0, 6.5, 8.0, 5.5, 7.0),   # Obstacle 21
    (2.0, 3.5, 3.0, 4.5, 7.5, 9.0),   # Obstacle 22
    (7.0, 8.5, 4.5, 6.0, 2.5, 4.0),   # Obstacle 23
    (4.0, 5.5, 8.0, 9.5, 3.0, 4.5),   # Obstacle 24
    (9.5, 10.5, 1.0, 2.5, 5.0, 6.5),  # Obstacle 25
    (3.5, 5.0, 5.5, 7.0, 1.0, 2.5),   # Obstacle 26
    (8.5, 10.0, 7.5, 9.0, 4.5, 6.0),  # Obstacle 27
    (1.0, 2.5, 6.0, 7.5, 8.0, 9.5),   # Obstacle 28
    (6.0, 7.5, 3.0, 4.5, 1.0, 2.5),   # Obstacle 29
    (4.5, 6.0, 7.5, 9.0, 2.0, 3.5),   # Obstacle 30
    ]
    
    
    '''
    # -----------------------
    #   Run basic RRT
    # -----------------------
    rrt_path = rrt_planning(
        start=start_coord,
        goal=end_coord,
        obstacles=obstacles,
        min_x=min_x, max_x=max_x,
        min_y=min_y, max_y=max_y,
        min_z=min_z, max_z=max_z,
        expand_dist=0.5,
        goal_sample_rate=0.01,
        max_iter=2000,
        goal_tolerance=1.0
    )

    # -----------------------
    #   Run RRT*
    # -----------------------
    rrt_star_path = rrt_star_planning(
        start=start_coord,
        goal=end_coord,
        obstacles=obstacles,
        min_x=min_x, max_x=max_x,
        min_y=min_y, max_y=max_y,
        min_z=min_z, max_z=max_z,
        expand_dist=0.5,
        goal_sample_rate=0.01,
        max_iter=2000,
        goal_tolerance=1.0,
        max_radius=2.0
    )

    if rrt_path is not None:
        print("RRT path found, length = {:.2f}".format(compute_path_length(rrt_path)))
    else:
        print("RRT failed to find a path.")

    if rrt_star_path is not None:
        print("RRT* path found, length = {:.2f}".format(compute_path_length(rrt_star_path)))
    else:
        print("RRT* failed to find a path.")

    # -----------------------
    #   Compare and Plot
    # -----------------------
    if rrt_path is not None:
        plot_rrt_3d(rrt_path, start_coord, end_coord, obstacles, 
                    min_x, max_x, min_y, max_y, min_z, max_z, 
                    title='RRT Path Planning', color='blue', label_path='RRT Path')

    if rrt_star_path is not None:
        plot_rrt_3d(rrt_star_path, start_coord, end_coord, obstacles, 
                    min_x, max_x, min_y, max_y, min_z, max_z, 
                    title='RRT* Path Planning', color='orange', label_path='RRT* Path')

    # Plot both in one figure for direct comparison
    if rrt_path is not None or rrt_star_path is not None:
        plot_comparison_3d(rrt_path, rrt_star_path, start_coord, end_coord, obstacles,
                           min_x, max_x, min_y, max_y, min_z, max_z)
        
        
    '''
    
    num_runs = 10000  # Number of times to run each algorithm
    
    # Storage for path lengths and computation times
    rrt_lengths = []
    rrt_times = []
    rrt_star_lengths = []
    rrt_star_times = []
    
    # Perform multiple runs with a progress bar
    for _ in tqdm(range(num_runs), desc="Running RRT and RRT* simulations"):
        # Measure time for RRT
        start_time = time.time()
        rrt_path = rrt_planning(
            start=start_coord,
            goal=end_coord,
            obstacles=obstacles,
            min_x=min_x, max_x=max_x,
            min_y=min_y, max_y=max_y,
            min_z=min_z, max_z=max_z,
            expand_dist=0.5,
            goal_sample_rate=0.01,
            max_iter=1000,
            goal_tolerance=1.0
        )
        end_time = time.time()
        if rrt_path is not None:
            rrt_lengths.append(compute_path_length(rrt_path))
            rrt_times.append(end_time - start_time)
        
        # Measure time for RRT*
        start_time = time.time()
        rrt_star_path = rrt_star_planning(
            start=start_coord,
            goal=end_coord,
            obstacles=obstacles,
            min_x=min_x, max_x=max_x,
            min_y=min_y, max_y=max_y,
            min_z=min_z, max_z=max_z,
            expand_dist=0.5,
            goal_sample_rate=0.01,
            max_iter=1000,
            goal_tolerance=1.0,
            max_radius=2.0
        )
        end_time = time.time()
        if rrt_star_path is not None:
            rrt_star_lengths.append(compute_path_length(rrt_star_path))
            rrt_star_times.append(end_time - start_time)
    
    # Compute means
    rrt_mean_length = np.mean(rrt_lengths)
    rrt_mean_time = np.mean(rrt_times)
    rrt_star_mean_length = np.mean(rrt_star_lengths)
    rrt_star_mean_time = np.mean(rrt_star_times)
    
    # Plot histograms for path lengths
    plt.figure(figsize=(12, 6))
    plt.hist(rrt_lengths, bins=20, alpha=0.7, label=f'RRT (Mean Length: {rrt_mean_length:.2f})')
    plt.hist(rrt_star_lengths, bins=20, alpha=0.7, label=f'RRT* (Mean Length: {rrt_star_mean_length:.2f})')
    plt.title("Path Lengths Distribution: RRT vs RRT*")
    plt.xlabel("Path Length")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid()
    plt.show()
    
    # Print average computation times
    print(f"Average computation time for RRT: {rrt_mean_time:.4f} seconds")
    print(f"Average computation time for RRT*: {rrt_star_mean_time:.4f} seconds")
