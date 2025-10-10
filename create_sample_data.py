"""Generate sample point cloud data for testing."""

import numpy as np
import open3d as o3d

def is_in_door(x, y, z):
    """Check if point is within door opening."""
    # Door on front wall (y=2.5), centered, 1m wide x 2.1m tall
    door_x_min, door_x_max = -0.5, 0.5
    door_z_min, door_z_max = 0, 2.1
    
    if abs(y - 2.5) < 0.1:  # Front wall
        if door_x_min <= x <= door_x_max and door_z_min <= z <= door_z_max:
            return True
    return False

def is_in_window(x, y, z):
    """Check if point is within window openings."""
    window_z_min, window_z_max = 1.2, 2.2  # Windows at 1.2m-2.2m height
    
    # Window 1: Left wall, centered
    if abs(x + 2.5) < 0.1:  # Left wall
        if -0.6 <= y <= 0.6 and window_z_min <= z <= window_z_max:
            return True
    
    # Window 2: Right wall, centered
    if abs(x - 2.5) < 0.1:  # Right wall
        if -0.6 <= y <= 0.6 and window_z_min <= z <= window_z_max:
            return True
    
    # Window 3: Back wall, offset to left
    if abs(y + 2.5) < 0.1:  # Back wall
        if -1.5 <= x <= -0.3 and window_z_min <= z <= window_z_max:
            return True
    
    return False

def create_sample_room():
    """Create a room with doors and windows."""
    points = []
    colors = []
    
    # Floor (5m x 5m)
    for x in np.linspace(-2.5, 2.5, 100):
        for y in np.linspace(-2.5, 2.5, 100):
            points.append([x, y, 0])
            colors.append([0.6, 0.4, 0.2])  # Brown floor
    
    # Ceiling (5m x 5m at 3m height)
    for x in np.linspace(-2.5, 2.5, 80):
        for y in np.linspace(-2.5, 2.5, 80):
            points.append([x, y, 3])
            colors.append([0.9, 0.9, 0.9])  # Light gray ceiling
    
    # Wall 1 (back wall) - with window
    for x in np.linspace(-2.5, 2.5, 100):
        for z in np.linspace(0, 3, 60):
            if not is_in_window(x, -2.5, z):
                points.append([x, -2.5, z])
                colors.append([0.95, 0.95, 0.95])  # White wall
    
    # Wall 2 (front wall) - with door
    for x in np.linspace(-2.5, 2.5, 100):
        for z in np.linspace(0, 3, 60):
            if not is_in_door(x, 2.5, z):
                points.append([x, 2.5, z])
                colors.append([0.95, 0.95, 0.95])  # White wall
    
    # Wall 3 (left wall) - with window
    for y in np.linspace(-2.5, 2.5, 100):
        for z in np.linspace(0, 3, 60):
            if not is_in_window(-2.5, y, z):
                points.append([-2.5, y, z])
                colors.append([0.95, 0.95, 0.95])  # White wall
    
    # Wall 4 (right wall) - with window
    for y in np.linspace(-2.5, 2.5, 100):
        for z in np.linspace(0, 3, 60):
            if not is_in_window(2.5, y, z):
                points.append([2.5, y, z])
                colors.append([0.95, 0.95, 0.95])  # White wall
    
    # Add door frame (brown wood)
    door_frame_thickness = 0.05
    door_x_min, door_x_max = -0.5, 0.5
    door_z_min, door_z_max = 0, 2.1
    
    # Door frame - left side
    for z in np.linspace(door_z_min, door_z_max, 40):
        for offset in np.linspace(-door_frame_thickness, door_frame_thickness, 3):
            points.append([door_x_min, 2.5 + offset, z])
            colors.append([0.4, 0.25, 0.1])  # Dark brown
    
    # Door frame - right side
    for z in np.linspace(door_z_min, door_z_max, 40):
        for offset in np.linspace(-door_frame_thickness, door_frame_thickness, 3):
            points.append([door_x_max, 2.5 + offset, z])
            colors.append([0.4, 0.25, 0.1])  # Dark brown
    
    # Door frame - top
    for x in np.linspace(door_x_min, door_x_max, 20):
        for offset in np.linspace(-door_frame_thickness, door_frame_thickness, 3):
            points.append([x, 2.5 + offset, door_z_max])
            colors.append([0.4, 0.25, 0.1])  # Dark brown
    
    # Add window frames (light blue glass effect)
    window_positions = [
        (-2.5, 0, 'x'),  # Left wall
        (2.5, 0, 'x'),   # Right wall
        (0, -2.5, 'y'),  # Back wall (offset)
    ]
    
    for wall_pos, center, axis in window_positions:
        if axis == 'x':
            # Vertical wall (x constant)
            for y in np.linspace(center - 0.6, center + 0.6, 25):
                for z in np.linspace(1.2, 2.2, 20):
                    # Add sparse points for glass effect
                    if np.random.random() < 0.3:
                        points.append([wall_pos, y, z])
                        colors.append([0.7, 0.85, 0.95])  # Light blue glass
        else:
            # Vertical wall (y constant)
            for x in np.linspace(-1.5, -0.3, 25):
                for z in np.linspace(1.2, 2.2, 20):
                    if np.random.random() < 0.3:
                        points.append([x, wall_pos, z])
                        colors.append([0.7, 0.85, 0.95])  # Light blue glass
    
    # Add some noise to make it realistic
    points = np.array(points)
    noise = np.random.normal(0, 0.01, points.shape)
    points += noise
    
    # Create point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(np.array(colors))
    
    return pcd

if __name__ == "__main__":
    print("Generating sample room point cloud...")
    pcd = create_sample_room()
    
    # Save to file
    output_path = "data/sample_room.ply"
    o3d.io.write_point_cloud(output_path, pcd)
    
    print(f"✓ Sample point cloud saved to: {output_path}")
    print(f"  Points: {len(pcd.points):,}")
    print(f"  Bounds: X[{np.min(np.asarray(pcd.points)[:, 0]):.2f}, {np.max(np.asarray(pcd.points)[:, 0]):.2f}]")
    print(f"          Y[{np.min(np.asarray(pcd.points)[:, 1]):.2f}, {np.max(np.asarray(pcd.points)[:, 1]):.2f}]")
    print(f"          Z[{np.min(np.asarray(pcd.points)[:, 2]):.2f}, {np.max(np.asarray(pcd.points)[:, 2]):.2f}]")
