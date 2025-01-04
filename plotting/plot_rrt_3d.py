import matplotlib.pyplot as plt
import numpy as np

def plot_rrt_3d(path, start, goal, obstacles,
                min_x, max_x, min_y, max_y, min_z, max_z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot start and goal
    ax.scatter(*start, color='green', s=100, label='Start')
    ax.scatter(*goal, color='red', s=100, label='Goal')

    # Plot obstacles as cubes
    for obstacle in obstacles:
        x_min, x_max, y_min, y_max, z_min, z_max = obstacle
        x_size = x_max - x_min
        y_size = y_max - y_min
        z_size = z_max - z_min
        ax.bar3d(x_min, y_min, z_min, x_size, y_size, z_size, color='gray', alpha=0.5)

    # Plot path if found
    if path:
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], path[:, 2], color='blue', linewidth=2, label='Path')
        ax.scatter(path[:, 0], path[:, 1], path[:, 2], color='blue', s=10)

    # Set plot limits and labels
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_zlim(min_z, max_z)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('3D RRT Path Planning')
    ax.legend()

    plt.show()
