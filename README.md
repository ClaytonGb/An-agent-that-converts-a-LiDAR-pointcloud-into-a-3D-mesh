# Multi-Agent LiDAR 3D Room Scanner

A multi-agent system for generating 3D images of rooms using phone LiDAR sensors.

## Features

- **LiDAR Data Capture Agent**: Handles point cloud data from iOS devices
- **Point Cloud Processing Agent**: Cleans and processes raw LiDAR data
- **3D Mesh Generation Agent**: Converts point clouds to 3D meshes
- **Visualization Agent**: Renders and exports 3D room models

## Requirements

- Python 3.8+
- iOS device with LiDAR (iPhone 12 Pro+, iPad Pro 2020+)
- Dependencies listed in `requirements.txt`

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py --input <lidar_data_file> --output <output_directory>
```

## Architecture

The system uses a multi-agent architecture where each agent specializes in a specific task:
1. Data ingestion and validation
2. Point cloud processing and filtering
3. Mesh generation and optimization
4. Rendering and export

## Supported Formats

- Input: PLY, LAS, PCD, XYZ (point cloud formats)
- Output: OBJ, STL, PLY, GLTF (3D model formats)

## License

MIT License - See LICENSE file for details
