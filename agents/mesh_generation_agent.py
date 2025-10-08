"""Agent responsible for generating 3D meshes from point clouds."""

import open3d as o3d
from typing import Optional
from .base_agent import BaseAgent


class MeshGenerationAgent(BaseAgent):
    """Agent for generating 3D meshes from point cloud data."""
    
    def __init__(self):
        """Initialize the mesh generation agent."""
        super().__init__("MeshGeneration")
    
    def process(self, pcd: o3d.geometry.PointCloud) -> Optional[o3d.geometry.TriangleMesh]:
        """Generate 3D mesh from point cloud.
        
        Args:
            pcd: Input point cloud with normals
            
        Returns:
            Generated triangle mesh or None if generation fails
        """
        if pcd is None or pcd.is_empty():
            self.log_error("Input point cloud is empty")
            return None
        
        if not pcd.has_normals():
            self.log_error("Point cloud must have normals for mesh generation")
            return None
        
        self.log_info(f"Generating mesh from {len(pcd.points):,} points")
        
        try:
            # Use Poisson surface reconstruction
            mesh = self.poisson_reconstruction(pcd)
            
            if mesh is None:
                self.log_warning("Poisson reconstruction failed, trying Ball Pivoting")
                mesh = self.ball_pivoting_reconstruction(pcd)
            
            if mesh is not None:
                # Clean up the mesh
                mesh = self.clean_mesh(mesh)
                self.log_info(f"Mesh generated: {len(mesh.vertices):,} vertices, "
                            f"{len(mesh.triangles):,} triangles")
            
            return mesh
            
        except Exception as e:
            self.log_error(f"Mesh generation failed: {str(e)}")
            return None
    
    def poisson_reconstruction(self, pcd: o3d.geometry.PointCloud, 
                               depth: int = 9) -> Optional[o3d.geometry.TriangleMesh]:
        """Generate mesh using Poisson surface reconstruction.
        
        Args:
            pcd: Input point cloud with normals
            depth: Octree depth for reconstruction
            
        Returns:
            Generated mesh or None
        """
        self.log_info("Running Poisson surface reconstruction...")
        
        try:
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                pcd, depth=depth
            )
            
            # Remove low-density vertices
            vertices_to_remove = densities < 0.01
            mesh.remove_vertices_by_mask(vertices_to_remove)
            
            return mesh
            
        except Exception as e:
            self.log_error(f"Poisson reconstruction failed: {str(e)}")
            return None
    
    def ball_pivoting_reconstruction(self, pcd: o3d.geometry.PointCloud) -> Optional[o3d.geometry.TriangleMesh]:
        """Generate mesh using Ball Pivoting Algorithm.
        
        Args:
            pcd: Input point cloud with normals
            
        Returns:
            Generated mesh or None
        """
        self.log_info("Running Ball Pivoting reconstruction...")
        
        try:
            # Estimate point cloud spacing
            distances = pcd.compute_nearest_neighbor_distance()
            avg_dist = sum(distances) / len(distances)
            
            # Set radii for ball pivoting
            radii = [avg_dist * r for r in [1, 2, 4]]
            
            mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
                pcd,
                o3d.utility.DoubleVector(radii)
            )
            
            return mesh
            
        except Exception as e:
            self.log_error(f"Ball Pivoting reconstruction failed: {str(e)}")
            return None
    
    def clean_mesh(self, mesh: o3d.geometry.TriangleMesh) -> o3d.geometry.TriangleMesh:
        """Clean and optimize mesh.
        
        Args:
            mesh: Input mesh
            
        Returns:
            Cleaned mesh
        """
        self.log_info("Cleaning mesh...")
        
        # Remove duplicated vertices and triangles
        mesh.remove_duplicated_vertices()
        mesh.remove_duplicated_triangles()
        mesh.remove_degenerate_triangles()
        mesh.remove_non_manifold_edges()
        
        # Compute vertex normals for smooth shading
        mesh.compute_vertex_normals()
        
        return mesh
