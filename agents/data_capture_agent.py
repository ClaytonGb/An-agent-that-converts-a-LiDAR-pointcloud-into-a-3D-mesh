"""Agent responsible for capturing and loading LiDAR data."""

import os
from typing import Optional
import numpy as np
import open3d as o3d
from .base_agent import BaseAgent


class DataCaptureAgent(BaseAgent):
    """Agent for capturing and loading LiDAR point cloud data."""
    
    def __init__(self):
        """Initialize the data capture agent."""
        super().__init__("DataCapture")
        self.supported_formats = ['.ply', '.pcd', '.las', '.xyz']
    
    def process(self, file_path: str) -> Optional[o3d.geometry.PointCloud]:
        """Load point cloud data from file.
        
        Args:
            file_path: Path to the point cloud file
            
        Returns:
            Open3D PointCloud object or None if loading fails
        """
        self.log_info(f"Loading point cloud from: {file_path}")
        
        if not os.path.exists(file_path):
            self.log_error(f"File not found: {file_path}")
            return None
        
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in self.supported_formats:
            self.log_error(f"Unsupported format: {file_ext}")
            return None
        
        try:
            # Load point cloud
            pcd = o3d.io.read_point_cloud(file_path)
            
            if pcd.is_empty():
                self.log_error("Loaded point cloud is empty")
                return None
            
            num_points = len(pcd.points)
            self.log_info(f"Successfully loaded {num_points:,} points")
            
            # Log basic statistics
            points = np.asarray(pcd.points)
            self.log_info(f"Point cloud bounds: "
                         f"X[{points[:, 0].min():.2f}, {points[:, 0].max():.2f}] "
                         f"Y[{points[:, 1].min():.2f}, {points[:, 1].max():.2f}] "
                         f"Z[{points[:, 2].min():.2f}, {points[:, 2].max():.2f}]")
            
            return pcd
            
        except Exception as e:
            self.log_error(f"Failed to load point cloud: {str(e)}")
            return None
    
    def validate_data(self, pcd: o3d.geometry.PointCloud) -> bool:
        """Validate point cloud data quality.
        
        Args:
            pcd: Point cloud to validate
            
        Returns:
            True if valid, False otherwise
        """
        if pcd is None or pcd.is_empty():
            self.log_error("Point cloud is empty")
            return False
        
        num_points = len(pcd.points)
        if num_points < 100:
            self.log_warning(f"Point cloud has very few points: {num_points}")
            return False
        
        self.log_info(f"Point cloud validation passed: {num_points:,} points")
        return True
