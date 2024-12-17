import random
import math

class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.parent = None

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def steer(from_node, to_point, expand_dist):
    dx = to_point[0] - from_node.x
    dy = to_point[1] - from_node.y
    dz = to_point[2] - from_node.z
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
    if dist < 1e-9:
        return Node(to_point[0], to_point[1], to_point[2])
    new_x = from_node.x + expand_dist * dx / dist
    new_y = from_node.y + expand_dist * dy / dist
    new_z = from_node.z + expand_dist * dz / dist
    return Node(new_x, new_y, new_z)

def check_collision(node_from, node_to, obstacles):
    seg_dist = distance((node_from.x, node_from.y, node_from.z),
                        (node_to.x, node_to.y, node_to.z))
    steps = int(seg_dist / 0.5) + 1
    for i in range(steps):
        t = i / float(steps)
        x = node_from.x + t * (node_to.x - node_from.x)
        y = node_from.y + t * (node_to.y - node_from.y)
        z = node_from.z + t * (node_to.z - node_from.z)

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
    if random.random() < goal_sample_rate:
        return (goal[0], goal[1], goal[2])
    else:
        rx = random.uniform(min_x, max_x)
        ry = random.uniform(min_y, max_y)
        rz = random.uniform(min_z, max_z)
        return (rx, ry, rz)

def backtrace_path(goal_node):
    path = []
    node = goal_node
    while node is not None:
        path.append((node.x, node.y, node.z))
        node = node.parent
    path.reverse()
    return path

def rrt_planning(start, goal, obstacles,
                 min_x, max_x, min_y, max_y, min_z, max_z,
                 expand_dist=1.0, goal_sample_rate=0.05,
                 max_iter=1000, goal_tolerance=1.0):
    start_node = Node(start[0], start[1], start[2])
    goal_node = Node(goal[0], goal[1], goal[2])
    node_list = [start_node]

    for _ in range(max_iter):
        rnd_point = generate_random_point(min_x, max_x, min_y, max_y, min_z, max_z, goal_sample_rate, goal)
        nearest_index = get_nearest_node_index(node_list, rnd_point)
        nearest_node = node_list[nearest_index]

        new_node = steer(nearest_node, rnd_point, expand_dist)
        if check_collision(nearest_node, new_node, obstacles):
            new_node.parent = nearest_node
            node_list.append(new_node)

            if distance((new_node.x, new_node.y, new_node.z),
                        (goal_node.x, goal_node.y, goal_node.z)) < goal_tolerance:
                goal_node.parent = new_node
                return backtrace_path(goal_node)

    return None