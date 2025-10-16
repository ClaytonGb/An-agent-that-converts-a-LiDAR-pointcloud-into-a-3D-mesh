"""Agent responsible for generating 3D meshes from point clouds.0018-9E2B F9C6-4645"""

import open3d as o3d
from typing import Optional
from .base_agent import BaseAgent
from config import MESH_CONFIG


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
                
                # Simplify mesh if configured
                if MESH_CONFIG['simplify_mesh']:
                    mesh = self.simplify_mesh(mesh)
                
                self.log_info(f"Mesh generated: {len(mesh.vertices):,} vertices, "
                            f"{len(mesh.triangles):,} triangles")
            
            return mesh
            
        except Exception as e:
            self.log_error(f"Mesh generation failed: {str(e)}")
            return None
    
    def poisson_reconstruction(self, pcd: o3d.geometry.PointCloud, 
                               depth: int = None) -> Optional[o3d.geometry.TriangleMesh]:
        """Generate mesh using Poisson surface reconstruction.
        
        Args:
            pcd: Input point cloud with normals
            depth: Octree depth for reconstruction (defaults to config value)
            
        Returns:
            Generated mesh or None
        """
        if depth is None:
            depth = MESH_CONFIG['poisson_depth']
            
        self.log_info("Running Poisson surface reconstruction...")
        
        try:
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                pcd, depth=depth
            )
            
            # Remove low-density vertices
            vertices_to_remove = densities < MESH_CONFIG['poisson_density_threshold']
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
            radii = [avg_dist * r for r in MESH_CONFIG['ball_pivot_radii_multipliers']]
            
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
    
    def simplify_mesh(self, mesh: o3d.geometry.TriangleMesh) -> o3d.geometry.TriangleMesh:
        """Simplify mesh by reducing triangle count.
        
        Args:
            mesh: Input mesh
            
        Returns:
            Simplified mesh
        """
        original_triangles = len(mesh.triangles)
        target_triangles = int(original_triangles * MESH_CONFIG['target_triangle_ratio'])
        
        self.log_info(f"Simplifying mesh from {original_triangles:,} to ~{target_triangles:,} triangles...")
        
        try:
            # Use quadric decimation for mesh simplification
            simplified_mesh = mesh.simplify_quadric_decimation(
                target_number_of_triangles=target_triangles
            )
            
            # Recompute normals after simplification
            simplified_mesh.compute_vertex_normals()
            
            self.log_info(f"Simplified to {len(simplified_mesh.triangles):,} triangles "
                         f"({len(simplified_mesh.triangles)/original_triangles*100:.1f}% of original)")
            
            return simplified_mesh
            
        except Exception as e:
            self.log_warning(f"Mesh simplification failed: {str(e)}, using original mesh")
            return mesh
