"""Agent responsible for processing and cleaning point cloud data."""

import numpy as np
import open3d as o3d
from typing import Optional, Tuple
from .base_agent import BaseAgent
from config import PROCESSING_CONFIG


class ProcessingAgent(BaseAgent):
    """Agent for processing and cleaning point cloud data."""
    
    def __init__(self):
        """Initialize the processing agent."""
        super().__init__("Processing")
    
    def process(self, pcd: o3d.geometry.PointCloud) -> Optional[o3d.geometry.PointCloud]:
        """Process and clean point cloud data.
        
        Args:
            pcd: Input point cloud
            
        Returns:
            Processed point cloud or None if processing fails
        """
        if pcd is None or pcd.is_empty():
            self.log_error("Input point cloud is empty")
            return None
        
        self.log_info(f"Processing point cloud with {len(pcd.points):,} points")
        
        try:
            # Step 1: Remove statistical outliers
            pcd_clean = self.remove_outliers(pcd)
            
            # Step 2: Downsample if too dense
            pcd_clean = self.downsample(pcd_clean)
            
            # Step 3: Estimate normals
            pcd_clean = self.estimate_normals(pcd_clean)
            
            self.log_info(f"Processing complete: {len(pcd_clean.points):,} points remaining")
            return pcd_clean
            
        except Exception as e:
            self.log_error(f"Processing failed: {str(e)}")
            return None
    
    def remove_outliers(self, pcd: o3d.geometry.PointCloud, 
                       nb_neighbors: int = None, 
                       std_ratio: float = None) -> o3d.geometry.PointCloud:
        """Remove statistical outliers from point cloud.
        
        Args:
            pcd: Input point cloud
            nb_neighbors: Number of neighbors to analyze (defaults to config value)
            std_ratio: Standard deviation ratio threshold (defaults to config value)
            
        Returns:
            Cleaned point cloud
        """
        if nb_neighbors is None:
            nb_neighbors = PROCESSING_CONFIG['outlier_nb_neighbors']
        if std_ratio is None:
            std_ratio = PROCESSING_CONFIG['outlier_std_ratio']
            
        self.log_info("Removing outliers...")
        
        cl, ind = pcd.remove_statistical_outlier(
            nb_neighbors=nb_neighbors,
            std_ratio=std_ratio
        )
        
        removed = len(pcd.points) - len(cl.points)
        self.log_info(f"Removed {removed:,} outlier points")
        
        return cl
    
    def downsample(self, pcd: o3d.geometry.PointCloud, 
                   voxel_size: float = None) -> o3d.geometry.PointCloud:
        """Downsample point cloud using voxel grid.
        
        Args:
            pcd: Input point cloud
            voxel_size: Size of voxel grid (defaults to config value)
            
        Returns:
            Downsampled point cloud
        """
        if voxel_size is None:
            voxel_size = PROCESSING_CONFIG['voxel_size']
            
        original_count = len(pcd.points)
        
        # Only downsample if point cloud is very dense
        if original_count > PROCESSING_CONFIG['downsample_threshold']:
            self.log_info(f"Downsampling point cloud (voxel size: {voxel_size})...")
            pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
            self.log_info(f"Downsampled from {original_count:,} to {len(pcd_down.points):,} points")
            return pcd_down
        else:
            self.log_info("Point cloud density acceptable, skipping downsampling")
            return pcd
    
    def estimate_normals(self, pcd: o3d.geometry.PointCloud, 
                        radius: float = None, 
                        max_nn: int = None) -> o3d.geometry.PointCloud:
        """Estimate normals for point cloud.
        
        Args:
            pcd: Input point cloud
            radius: Search radius for normal estimation (defaults to config value)
            max_nn: Maximum number of nearest neighbors (defaults to config value)
            
        Returns:
            Point cloud with estimated normals
        """
        if radius is None:
            radius = PROCESSING_CONFIG['normal_radius']
        if max_nn is None:
            max_nn = PROCESSING_CONFIG['normal_max_nn']
            
        self.log_info("Estimating normals...")
        
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(
                radius=radius,
                max_nn=max_nn
            )
        )
        
        # Orient normals consistently
        pcd.orient_normals_consistent_tangent_plane(k=PROCESSING_CONFIG['normal_orient_k'])
        
        self.log_info("Normal estimation complete")
        return pcd
