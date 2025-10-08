"""Unit tests for DataCaptureAgent."""

import unittest
import os
import tempfile
import numpy as np
import open3d as o3d
from agents.data_capture_agent import DataCaptureAgent


class TestDataCaptureAgent(unittest.TestCase):
    """Test cases for DataCaptureAgent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = DataCaptureAgent()
        
    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        self.assertEqual(self.agent.name, "DataCapture")
        self.assertEqual(self.agent.supported_formats, ['.ply', '.pcd', '.las', '.xyz'])
    
    def test_validate_data_with_empty_pointcloud(self):
        """Test validation fails with empty point cloud."""
        pcd = o3d.geometry.PointCloud()
        self.assertFalse(self.agent.validate_data(pcd))
    
    def test_validate_data_with_none(self):
        """Test validation fails with None."""
        self.assertFalse(self.agent.validate_data(None))
    
    def test_validate_data_with_few_points(self):
        """Test validation fails with too few points."""
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(np.random.rand(50, 3))
        self.assertFalse(self.agent.validate_data(pcd))
    
    def test_validate_data_with_sufficient_points(self):
        """Test validation passes with sufficient points."""
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(np.random.rand(1000, 3))
        self.assertTrue(self.agent.validate_data(pcd))
    
    def test_process_nonexistent_file(self):
        """Test that processing nonexistent file returns None."""
        result = self.agent.process("nonexistent_file.ply")
        self.assertIsNone(result)
    
    def test_process_unsupported_format(self):
        """Test that processing unsupported format returns None."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            result = self.agent.process(temp_file)
            self.assertIsNone(result)
        finally:
            os.unlink(temp_file)
    
    def test_process_valid_ply_file(self):
        """Test processing a valid PLY file."""
        # Create a temporary PLY file
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(np.random.rand(1000, 3))
        
        with tempfile.NamedTemporaryFile(suffix='.ply', delete=False) as f:
            temp_file = f.name
        
        try:
            o3d.io.write_point_cloud(temp_file, pcd)
            result = self.agent.process(temp_file)
            
            self.assertIsNotNone(result)
            self.assertIsInstance(result, o3d.geometry.PointCloud)
            self.assertEqual(len(result.points), 1000)
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()

