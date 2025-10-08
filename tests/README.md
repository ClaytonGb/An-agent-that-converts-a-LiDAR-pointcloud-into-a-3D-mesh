# Tests

Unit tests for the Multi-Agent LiDAR 3D Room Scanner.

## Running Tests

Run all tests:
```bash
python -m unittest discover tests
```

Run a specific test file:
```bash
python -m unittest tests.test_data_capture_agent
```

Run with verbose output:
```bash
python -m unittest discover tests -v
```

## Test Coverage

- `test_base_agent.py`: Tests for the BaseAgent abstract class
- `test_data_capture_agent.py`: Tests for LiDAR data loading and validation
- `test_processing_agent.py`: Tests for point cloud processing operations

## Requirements

Tests require the same dependencies as the main application (see `requirements.txt`).

