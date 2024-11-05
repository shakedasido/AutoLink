# AutoLink: Autonomous Wheelchair Attachment System

AutoLink is an embedded real-time control system that autonomously navigates and connects a motorized device to a manual wheelchair, transforming it into an electric wheelchair with remote-control capabilities. This project uses computer vision, GPIO control, and an intuitive pathing algorithm to provide a practical and cost-effective assistive solution that enhances user independence.

## Table of Contents

- [Overview](#overview)
- [Project Goals](#project-goals)
- [System Architecture](#system-architecture)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Code Structure](#code-structure)
- [Usage](#usage)
- [Future Development](#future-development)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

AutoLink enables manual wheelchairs to transform into motorized versions by autonomously attaching a motorized device. This embedded system leverages a Raspberry Pi 4, Python, and computer vision to detect ArUco markers attached to wheelchairs, locate the wheelchair in real time, and control motor movement for precise navigation and alignment.

## Project Goals

- **Enhance Accessibility**: Provide an affordable, autonomous solution for converting manual wheelchairs into motorized ones, supporting user independence.
- **Minimize Manual Effort**: The system autonomously navigates and attaches the motorized device to the wheelchair, eliminating the need for human intervention.
- **Modular and Scalable Design**: Future-proof the project with modular code, allowing for easy updates and expansions, such as remote control or mobile app compatibility.

## System Architecture

AutoLink’s architecture comprises several components working together for real-time autonomous navigation and attachment. The main components include:

1. **Raspberry Pi 4**: Acts as the control hub, processing camera inputs, running control algorithms, and communicating with motors via GPIO.
2. **Camera and Computer Vision (ArUco Markers)**: The camera continuously scans for ArUco markers on wheelchairs, detecting position and orientation.
3. **GPIO and PWM Motor Control**: The Raspberry Pi’s GPIO pins control the motors, using PWM (Pulse Width Modulation) for smooth acceleration and precise movement.
4. **Keyboard Interface (Temporary Control)**: Provides manual control for testing and navigation until a dedicated remote control or app is implemented.

## Hardware Requirements

- **Raspberry Pi 4** (with Raspbian OS installed)
- **Camera Module** compatible with Raspberry Pi
- **Motors**: Right and left motors for navigation
- **GPIO-Compatible Components** for motor control (wiring, connectors, etc.)
- **ArUco Marker(s)** for positional tracking on the wheelchair

## Software Requirements

- **Python 3.7+**
- **OpenCV** with ArUco module (for marker detection)
- **RPi.GPIO**: For GPIO control
- **NumPy**: For array handling and mathematical calculations

### Python Dependencies

Install all required packages using pip:

```bash
pip install opencv-python RPi.GPIO numpy
```

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://[https://github.com/shakedasido/AutoLink.git]
   cd AutoLink
   ```

2. **Place ArUco Markers** on the wheelchair in locations that are visible to the camera. Make sure to measure the size of the marker for calibration.

3. **Run Initial Camera Calibration**: Calibrate the camera using a checkerboard pattern to correct any distortion (if calibration data is not already provided). This step ensures accurate detection and positioning of the wheelchair.

## Code Structure

- **main.py**: The main entry point of the project.
- **aruco_detection.py**: Handles ArUco marker detection, decoding the location and orientation of the wheelchair.
- **mapping_processing.py**: Translates image-based coordinates into real-world positioning, guiding the device toward the wheelchair.
- **GPIO_activation.py**: Manages GPIO pins and PWM signals for motor control, handling forward, backward, and directional movement.
- **keyboard_control.py**: Provides a temporary interface for manual control using keyboard input.
- **arrays.npz**: Calibration data for the camera.

### Module Descriptions

- **`aruco_detection.py`**: Uses OpenCV’s ArUco library to detect markers, calculate distance, and send orientation data to the main program.
- **`mapping_processing.py`**: Contains logic to convert detected marker positions into real-world coordinates, enabling accurate movement.
- **`GPIO_activation.py`**: Controls GPIO outputs, managing motor speed, direction, and attachment mechanisms through PWM and digital signals.
- **`keyboard_control.py`**: Allows manual testing and control via keyboard, useful for debugging and development before remote control implementation.

## Usage

1. **Start the System**:

   ```bash
   python main.py
   ```

2. **Testing Manual Control**:

   Use the keyboard to manually control the motors, with specific keys mapped to forward, backward, left, right, and attach/detach functions.

3. **Autonomous Operation**:

   When a marker is detected, the system will calculate the optimal path, adjust motor speeds and directions, and move toward the wheelchair to complete the attachment autonomously.

### Key Controls (for Keyboard Interface)

- **Up Arrow**: Move forward
- **Down Arrow**: Move backward
- **Left Arrow**: Turn left
- **Right Arrow**: Turn right
- **U/Y**: Control arm movement for attachment
- **L**: Toggle latch mechanism
- **C**: Connection mode - switches to automatic connection attempt mode to the wheelchair
- **D**: Disconnect mode - disconnects and travels back a little

## Future Development

AutoLink is designed with modularity and scalability in mind. Future improvements could include:

- **Remote Control or Mobile App**: Replace the keyboard interface with a dedicated remote control or a mobile app for greater ease of use.
- **Enhanced Physical Components**: Improve the device’s physical design with wheels that offer greater traction, and ensure all mechanical parts are compatible for optimal performance.
- **Public Deployment**: Adapt AutoLink for use in public spaces like nursing homes and malls, allowing multiple users to access the device as needed.
- **Safety Features**: Incorporate proximity sensors and collision avoidance to enhance safety in crowded spaces.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

