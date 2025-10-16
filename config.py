"""Configuration file for Multi-Agent LiDAR 3D Room Scanner."""

# Processing Agent Configuration
PROCESSING_CONFIG = {
    # Outlier removal parameters
    'outlier_nb_neighbors': 20,
    'outlier_std_ratio': 2.0,
    
    # Downsampling parameters
    'voxel_size': 0.02,
    'downsample_threshold': 100000,  # Only downsample if point count exceeds this
    
    # Normal estimation parameters
    'normal_radius': 0.1,
    'normal_max_nn': 30,
    'normal_orient_k': 15,
}

# Mesh Generation Agent Configuration
MESH_CONFIG = {
    # Poisson reconstruction parameters
    'poisson_depth': 9,
    'poisson_density_threshold': 0.01,
    
    # Ball pivoting parameters
    'ball_pivot_radii_multipliers': [1, 2, 4],
    
    # Mesh simplification parameters
    'simplify_mesh': True,
    'target_triangle_ratio': 0.3,  # Reduce triangles to 30% of original count
}

# Visualization Agent Configuration
VISUALIZATION_CONFIG = {
    # Render settings
    'background_color': [0.1, 0.1, 0.1],
    'point_size': 2.0,
    
    # Image rendering settings
    'render_width': 1920,
    'render_height': 1080,
    'render_background_color': [1, 1, 1],
}

# Data Validation Configuration
VALIDATION_CONFIG = {
    'min_points': 100,  # Minimum number of points required for valid point cloud
}

