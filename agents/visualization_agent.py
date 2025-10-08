"""Agent responsible for visualizing and exporting 3D models."""

import os
import open3d as o3d
import numpy as np
from typing import Optional, Union
from .base_agent import BaseAgent


class VisualizationAgent(BaseAgent):
    """Agent for visualizing and exporting 3D models."""
    
    def __init__(self):
        """Initialize the visualization agent."""
        super().__init__("Visualization")
        self.supported_export_formats = ['.obj', '.ply', '.stl', '.gltf', '.glb']
    
    def process(self, geometry: Union[o3d.geometry.PointCloud, o3d.geometry.TriangleMesh],
                output_path: Optional[str] = None) -> bool:
        """Visualize and optionally export geometry.
        
        Args:
            geometry: Point cloud or mesh to visualize
            output_path: Optional path to export the model
            
        Returns:
            True if successful, False otherwise
        """
        if geometry is None:
            self.log_error("Input geometry is None")
            return False
        
        try:
            # Visualize
            self.visualize(geometry)
            
            # Export if path provided
            if output_path:
                return self.export(geometry, output_path)
            
            return True
            
        except Exception as e:
            self.log_error(f"Visualization failed: {str(e)}")
            return False
    
    def visualize(self, geometry: Union[o3d.geometry.PointCloud, o3d.geometry.TriangleMesh]):
        """Display geometry in 3D viewer.
        
        Args:
            geometry: Geometry to visualize
        """
        self.log_info("Opening 3D viewer...")
        
        # Create visualizer
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name="LiDAR 3D Room Scan")
        
        # Add geometry
        vis.add_geometry(geometry)
        
        # Set rendering options
        opt = vis.get_render_option()
        opt.background_color = np.asarray([0.1, 0.1, 0.1])
        opt.point_size = 2.0
        
        # Run visualizer
        vis.run()
        vis.destroy_window()
    
    def export(self, geometry: Union[o3d.geometry.PointCloud, o3d.geometry.TriangleMesh],
               output_path: str) -> bool:
        """Export geometry to file.
        
        Args:
            geometry: Geometry to export
            output_path: Path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        file_ext = os.path.splitext(output_path)[1].lower()
        
        if file_ext not in self.supported_export_formats:
            self.log_error(f"Unsupported export format: {file_ext}")
            return False
        
        self.log_info(f"Exporting to: {output_path}")
        
        try:
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir:  # Only create directory if path includes a directory
                os.makedirs(output_dir, exist_ok=True)
            
            # Export based on geometry type
            if isinstance(geometry, o3d.geometry.PointCloud):
                success = o3d.io.write_point_cloud(output_path, geometry)
            elif isinstance(geometry, o3d.geometry.TriangleMesh):
                success = o3d.io.write_triangle_mesh(output_path, geometry)
            else:
                self.log_error(f"Unsupported geometry type: {type(geometry)}")
                return False
            
            if success:
                self.log_info(f"Successfully exported to {output_path}")
            else:
                self.log_error("Export failed")
            
            return success
            
        except Exception as e:
            self.log_error(f"Export failed: {str(e)}")
            return False
    
    def render_image(self, geometry: Union[o3d.geometry.PointCloud, o3d.geometry.TriangleMesh],
                     output_path: str, width: int = 1920, height: int = 1080) -> bool:
        """Render geometry to image file.
        
        Args:
            geometry: Geometry to render
            output_path: Path to save the image
            width: Image width
            height: Image height
            
        Returns:
            True if successful, False otherwise
        """
        self.log_info(f"Rendering image ({width}x{height})...")
        
        try:
            vis = o3d.visualization.Visualizer()
            vis.create_window(visible=False, width=width, height=height)
            vis.add_geometry(geometry)
            
            # Set rendering options
            opt = vis.get_render_option()
            opt.background_color = np.asarray([1, 1, 1])
            opt.point_size = 2.0
            
            # Update and capture
            vis.poll_events()
            vis.update_renderer()
            vis.capture_screen_image(output_path)
            vis.destroy_window()
            
            self.log_info(f"Image saved to: {output_path}")
            return True
            
        except Exception as e:
            self.log_error(f"Image rendering failed: {str(e)}")
            return False
