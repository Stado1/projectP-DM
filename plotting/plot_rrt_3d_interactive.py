import numpy as np
import plotly.graph_objects as go

def plot_rrt_3d_interactive(path, start, goal, obstacles,
                            min_x, max_x, min_y, max_y, min_z, max_z):
    fig = go.Figure()

    # Start and goal
    fig.add_trace(go.Scatter3d(
        x=[start[0]], y=[start[1]], z=[start[2]], mode='markers',
        marker=dict(size=6, color='green'), name='Start'
    ))
    fig.add_trace(go.Scatter3d(
        x=[goal[0]], y=[goal[1]], z=[goal[2]], mode='markers',
        marker=dict(size=6, color='red'), name='Goal'
    ))

    # Obstacles
    for obstacle in obstacles:
        x_min, x_max, y_min, y_max, z_min, z_max = obstacle
        vertices = [
            [x_min, y_min, z_min], [x_max, y_min, z_min], [x_max, y_max, z_min], [x_min, y_max, z_min],
            [x_min, y_min, z_max], [x_max, y_min, z_max], [x_max, y_max, z_max], [x_min, y_max, z_max]
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        for edge in edges:
            fig.add_trace(go.Scatter3d(
                x=[vertices[edge[0]][0], vertices[edge[1]][0]],
                y=[vertices[edge[0]][1], vertices[edge[1]][1]],
                z=[vertices[edge[0]][2], vertices[edge[1]][2]],
                mode='lines',
                line=dict(color='gray', width=5),
                showlegend=False
            ))

    # Path
    if path:
        path = np.array(path)
        fig.add_trace(go.Scatter3d(
            x=path[:, 0], y=path[:, 1], z=path[:, 2],
            mode='lines+markers', line=dict(color='blue', width=5),
            marker=dict(size=4, color='blue'), name='Path'
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title='X axis',
            yaxis_title='Y axis',
            zaxis_title='Z axis',
            xaxis=dict(range=[min_x, max_x]),
            yaxis=dict(range=[min_y, max_y]),
            zaxis=dict(range=[min_z, max_z])
        ),
        title='Interactive 3D RRT Path Planning',
        showlegend=True
    )

    fig.show(renderer="browser")
