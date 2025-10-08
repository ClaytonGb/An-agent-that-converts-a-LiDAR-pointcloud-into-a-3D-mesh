"""Main entry point for the multi-agent LiDAR 3D room scanner."""

import argparse
import os
import sys
from agents import DataCaptureAgent, ProcessingAgent, MeshGenerationAgent, VisualizationAgent


def main():
    """Run the multi-agent LiDAR scanning pipeline."""
    parser = argparse.ArgumentParser(
        description='Multi-Agent LiDAR 3D Room Scanner'
    )
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Path to input LiDAR point cloud file (PLY, PCD, LAS, XYZ)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Path to output 3D model file (OBJ, PLY, STL, GLTF)'
    )
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Display 3D visualization'
    )
    parser.add_argument(
        '--render',
        type=str,
        help='Path to save rendered image'
    )
    parser.add_argument(
        '--skip-mesh',
        action='store_true',
        help='Skip mesh generation (only process point cloud)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    print("=" * 60)
    print("Multi-Agent LiDAR 3D Room Scanner")
    print("=" * 60)
    
    # Initialize agents
    data_agent = DataCaptureAgent()
    processing_agent = ProcessingAgent()
    mesh_agent = MeshGenerationAgent()
    viz_agent = VisualizationAgent()
    
    # Step 1: Load point cloud data
    print("\n[1/4] Loading LiDAR data...")
    pcd = data_agent.process(args.input)
    
    if pcd is None or not data_agent.validate_data(pcd):
        print("Error: Failed to load or validate point cloud data")
        sys.exit(1)
    
    # Step 2: Process point cloud
    print("\n[2/4] Processing point cloud...")
    pcd_processed = processing_agent.process(pcd)
    
    if pcd_processed is None:
        print("Error: Point cloud processing failed")
        sys.exit(1)
    
    # Step 3: Generate mesh (optional)
    mesh = None
    if not args.skip_mesh:
        print("\n[3/4] Generating 3D mesh...")
        mesh = mesh_agent.process(pcd_processed)
        
        if mesh is None:
            print("Warning: Mesh generation failed, will use point cloud instead")
    else:
        print("\n[3/4] Skipping mesh generation (--skip-mesh flag set)")
    
    # Step 4: Visualize and export
    print("\n[4/4] Visualization and export...")
    
    # Determine what to visualize/export
    geometry = mesh if mesh is not None else pcd_processed
    
    # Export if output path provided
    if args.output:
        success = viz_agent.export(geometry, args.output)
        if not success:
            print("Error: Export failed")
            sys.exit(1)
    
    # Render image if requested
    if args.render:
        success = viz_agent.render_image(geometry, args.render)
        if not success:
            print("Warning: Image rendering failed")
    
    # Visualize if requested
    if args.visualize:
        viz_agent.visualize(geometry)
    
    print("\n" + "=" * 60)
    print("Processing complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
