"""Generate sample point cloud data for testing."""

import numpy as np
import open3d as o3d

def create_sample_room():
    """Create a simple room-like point cloud."""
    points = []
    
    # Floor (5m x 5m)
    for x in np.linspace(-2.5, 2.5, 100):
        for y in np.linspace(-2.5, 2.5, 100):
            points.append([x, y, 0])
    
    # Ceiling (5m x 5m at 3m height)
    for x in np.linspace(-2.5, 2.5, 80):
        for y in np.linspace(-2.5, 2.5, 80):
            points.append([x, y, 3])
    
    # Wall 1 (back wall)
    for x in np.linspace(-2.5, 2.5, 100):
        for z in np.linspace(0, 3, 60):
            points.append([x, -2.5, z])
    
    # Wall 2 (front wall)
    for x in np.linspace(-2.5, 2.5, 100):
        for z in np.linspace(0, 3, 60):
            points.append([x, 2.5, z])
    
    # Wall 3 (left wall)
    for y in np.linspace(-2.5, 2.5, 100):
        for z in np.linspace(0, 3, 60):
            points.append([-2.5, y, z])
    
    # Wall 4 (right wall)
    for y in np.linspace(-2.5, 2.5, 100):
        for z in np.linspace(0, 3, 60):
            points.append([2.5, y, z])
    
    # Add some noise to make it realistic
    points = np.array(points)
    noise = np.random.normal(0, 0.01, points.shape)
    points += noise
    
    # Create point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    # Add colors (walls = white, floor = brown, ceiling = light gray)
    colors = []
    for point in points:
        if abs(point[2]) < 0.1:  # Floor
            colors.append([0.6, 0.4, 0.2])
        elif abs(point[2] - 3) < 0.1:  # Ceiling
            colors.append([0.9, 0.9, 0.9])
        else:  # Walls
            colors.append([0.95, 0.95, 0.95])
    
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
