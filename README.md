# Fall Detection from Smartwatch Data

This repository contains a fall detection system that analyzes accelerometer and gyroscope data from a smartwatch to identify falls and trigger an emergency response. The system uses a Kalman filter to fuse sensor data, a Finite State Machine (FSM) to track user activity states, and a Decision Tree to define the FSM's transition rules.

## Features
- **Signal Processing**: Computes the Signal Vector Magnitude (SVM), a robust pitch angle by fusing gyroscope and accelerometer data with a Kalman filter, and the Gyroscope Vector Magnitude (GVM) or angular speed.
- **State Detection**: A Finite State Machine (FSM) is used to detect the user's state, transitioning between "walking," "jogging," "prefall," and "fall."
- **Emergency Response**: Upon detecting a fall, the system enters an "alarm" state to prompt the user for their status.
    - If the user is safe, the system registers a false alarm and returns to its normal "running" state.
    - If the user is not safe or does not respond within a predefined timeout period, the system escalates to an "emergency" state, activating safety protocols like a wearable alert signal.
- **Decision Tree**: The transition rules for the FSM are defined using a Decision Tree created in the `activity_detection.ipynb` Jupyter notebook.


## Installation
This project uses `uv` as the dependency manager.


1. **Install uv**: Follow the official instructions to install `uv` from [astral-sh/uv](https://github.com/astral-sh/uv).
2. **Clone the repository**:
```bash
git clone https://github.com/nicol-buratti/fall-detection.git
cd fall-detection
```
3. **Install dependencies**
```bash
uv sync
```

## Usage
1. **Generate Data**: Use the provided scripts to generate and process the data.
```bash
uv run generate_raw_data_csv.py
uv run generate_data_for_ptolemy.py
```
2. **Analyze and Model**:
    - Open and run the `activity_detection.ipynb` notebook to see how the Decision Tree and FSM transition rules are generated.
    - The `model_fall_detection.xml` file can be used with [Ptolemy II](https://ptolemy.berkeley.edu/ptolemyII/index.htm) to simulate and test the fall detection model.

## License
This project is licensed under the AGPL-3.0 License. See the LICENSE file for details.
