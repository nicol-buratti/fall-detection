# Fall Detection from smartwatch data

Fall detection system using sensor data from smartwatch. It includes scripts for data processing, a Jupyter Notebook for activity detection, and a model for use with the Ptolemy II program.

## Installation
This project uses uv, a fast Python package manager.

1. **Install uv**: Follow the official instructions to install uv: https://github.com/astral-sh/uv
2. **Install dependency**
```bash
uv sync
```
2. **Run the scripts**
```bash
uv run generate_raw_data_csv.py
```

## Usage

- **Data Generation**:
    - `generate_raw_data_csv.py`: Generates raw sensor data.

    - `generate_data_for_ptolemy.py`: Converts data into Ptolemy II-compatible format.

- **Model**: `model_fall_detection.xml` defines the fall detection model for Ptolemy II simulation.

- **Analysis**: `activity_detection.ipynb`: Jupyter Notebook for analyzing activity data.