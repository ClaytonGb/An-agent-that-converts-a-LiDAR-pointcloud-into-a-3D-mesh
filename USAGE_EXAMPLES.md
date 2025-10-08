# Usage Examples

This guide provides practical examples for using the Multi-Agent LiDAR 3D Room Scanner.

## Basic Usage

### 1. Simple Point Cloud Processing

Process a LiDAR scan and visualize it:

```bash
python main.py --input data/room_scan.ply --visualize
```

### 2. Generate 3D Mesh from Point Cloud

Convert point cloud to mesh and export:

```bash
python main.py --input data/room_scan.ply --output models/room_mesh.obj
```

### 3. Full Pipeline with Visualization

Process, generate mesh, export, and visualize:

```bash
python main.py --input data/room_scan.ply --output models/room.obj --visualize
```

### 4. Render Static Image

Generate a rendered image of the 3D model:

```bash
python main.py --input data/room_scan.ply --render renders/room_view.png
```

### 5. Point Cloud Only (Skip Mesh Generation)

Process point cloud without mesh generation:

```bash
python main.py --input data/room_scan.ply --output processed/room.pcd --skip-mesh
```

## Advanced Examples

### Batch Processing Multiple Rooms

```bash
#!/bin/bash
for file in data/scans/*.ply; do
    filename=$(basename "$file" .ply)
    python main.py --input "$file" --output "models/${filename}.obj" --render "renders/${filename}.png"
done
```

### Processing with Custom Configuration

Modify `config.py` to adjust processing parameters:

```python
# config.py
VOXEL_SIZE = 0.02  # Adjust for different point cloud densities
OUTLIER_NEIGHBORS = 20  # Increase for noisier data
MESH_DEPTH = 9  # Higher = more detailed mesh
```

Then run:

```bash
python main.py --input data/detailed_scan.ply --output models/detailed_room.obj
```

## Supported File Formats

### Input Formats
- **PLY** (Polygon File Format) - Recommended
- **PCD** (Point Cloud Data)
- **LAS** (LASer file format)
- **XYZ** (ASCII point cloud)

### Output Formats
- **OBJ** (Wavefront) - Best for general 3D software
- **PLY** (Polygon File Format) - Preserves color data
- **STL** (Stereolithography) - For 3D printing
- **GLTF** (GL Transmission Format) - For web/AR applications

## Capturing LiDAR Data from iPhone/iPad

### Recommended Apps

1. **3D Scanner App** (Free)
   - Export as PLY format
   - Good for room-scale scanning

2. **Polycam** (Free/Premium)
   - High-quality exports
   - Supports multiple formats

3. **Record3D** (Free/Premium)
   - Real-time streaming
   - Export point clouds

### Best Practices for Scanning

1. **Lighting**: Ensure good lighting in the room
2. **Movement**: Move slowly and steadily
3. **Coverage**: Scan all areas including corners
4. **Distance**: Stay 1-3 meters from surfaces
5. **Overlap**: Ensure 30-50% overlap between scan positions

## Troubleshooting

### Issue: "Failed to load point cloud data"
**Solution**: Verify file format and ensure it's not corrupted

```bash
# Check file format
file data/room_scan.ply
```

### Issue: Mesh generation produces poor results
**Solution**: Adjust mesh depth in config.py

```python
MESH_DEPTH = 8  # Try lower values for simpler geometry
```

### Issue: Point cloud is too dense/sparse
**Solution**: Adjust voxel size for downsampling

```python
VOXEL_SIZE = 0.05  # Increase for more downsampling
```

## Performance Tips

1. **Large Point Clouds**: Use `--skip-mesh` for initial validation
2. **Memory Issues**: Increase voxel size to reduce point count
3. **Faster Processing**: Reduce `OUTLIER_NEIGHBORS` in config
4. **Better Quality**: Increase `MESH_DEPTH` (slower but more detailed)

## Integration Examples

### Using as a Python Module

```python
from agents import DataCaptureAgent, ProcessingAgent, MeshGenerationAgent

# Initialize agents
data_agent = DataCaptureAgent()
processing_agent = ProcessingAgent()
mesh_agent = MeshGenerationAgent()

# Process data
pcd = data_agent.process("data/room.ply")
pcd_processed = processing_agent.process(pcd)
mesh = mesh_agent.process(pcd_processed)
```

### Custom Pipeline

```python
import open3d as o3d
from agents import ProcessingAgent, VisualizationAgent

# Load your own point cloud
pcd = o3d.io.read_point_cloud("custom_data.pcd")

# Process with custom parameters
processing_agent = ProcessingAgent()
pcd_clean = processing_agent.process(pcd)

# Visualize
viz_agent = VisualizationAgent()
viz_agent.visualize(pcd_clean)
```

## Contributing

When adding new features or examples, please:
1. Test with multiple input formats
2. Update this documentation
3. Add unit tests in `tests/` directory
4. Follow the existing code style

## Support

For issues or questions:
- Check existing GitHub issues
- Review test files for usage patterns
- Consult agent documentation in source files
