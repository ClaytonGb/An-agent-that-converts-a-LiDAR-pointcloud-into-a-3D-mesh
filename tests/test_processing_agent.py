"""Unit tests for ProcessingAgent."""

import unittest
import numpy as np
import open3d as o3d
from agents.processing_agent import ProcessingAgent


class TestProcessingAgent(unittest.TestCase):
    """Test cases for ProcessingAgent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = ProcessingAgent()
        
        # Create a sample point cloud for testing
        self.pcd = o3d.geometry.PointCloud()
        points = np.random.rand(1000, 3)
        self.pcd.points = o3d.utility.Vector3dVector(points)
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        self.assertEqual(self.agent.name, "Processing")
    
    def test_process_with_none(self):
        """Test that processing None returns None."""
        result = self.agent.process(None)
        self.assertIsNone(result)
    
    def test_process_with_empty_pointcloud(self):
        """Test that processing empty point cloud returns None."""
        empty_pcd = o3d.geometry.PointCloud()
        result = self.agent.process(empty_pcd)
        self.assertIsNone(result)
    
    def test_process_valid_pointcloud(self):
        """Test processing a valid point cloud."""
        result = self.agent.process(self.pcd)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, o3d.geometry.PointCloud)
        self.assertTrue(result.has_normals())
    
    def test_remove_outliers(self):
        """Test outlier removal."""
        # Add some extreme outliers
        points = np.asarray(self.pcd.points)
        outliers = np.array([[100, 100, 100], [-100, -100, -100]])
        all_points = np.vstack([points, outliers])
        
        pcd_with_outliers = o3d.geometry.PointCloud()
        pcd_with_outliers.points = o3d.utility.Vector3dVector(all_points)
        
        result = self.agent.remove_outliers(pcd_with_outliers)
        
        self.assertIsNotNone(result)
        # Should have removed the outliers
        self.assertLess(len(result.points), len(pcd_with_outliers.points))
    
    def test_downsample_small_pointcloud(self):
        """Test that small point clouds are not downsampled."""
        small_pcd = o3d.geometry.PointCloud()
        small_pcd.points = o3d.utility.Vector3dVector(np.random.rand(5000, 3))
        
        result = self.agent.downsample(small_pcd)
        
        # Should not be downsampled (threshold is 100,000)
        self.assertEqual(len(result.points), 5000)
    
    def test_downsample_large_pointcloud(self):
        """Test that large point clouds are downsampled."""
        large_pcd = o3d.geometry.PointCloud()
        large_pcd.points = o3d.utility.Vector3dVector(np.random.rand(150000, 3))
        
        result = self.agent.downsample(large_pcd, voxel_size=0.05)
        
        # Should be downsampled
        self.assertLess(len(result.points), 150000)
    
    def test_estimate_normals(self):
        """Test normal estimation."""
        result = self.agent.estimate_normals(self.pcd)
        
        self.assertIsNotNone(result)
        self.assertTrue(result.has_normals())
        self.assertEqual(len(result.normals), len(result.points))


if __name__ == '__main__':
    unittest.main()

