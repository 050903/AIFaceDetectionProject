# Drowsiness Detection System

<div align="center">
![image](https://github.com/user-attachments/assets/af6d0ffd-3459-40b2-959c-8238487d34d5)
  <p><strong>An intelligent system for monitoring driver drowsiness using computer vision</strong></p>
</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Configuration Parameters](#configuration-parameters)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

The Drowsiness Detection System is an application that utilizes computer vision and machine learning to detect drowsiness in drivers. The system continuously monitors for signs of drowsiness such as prolonged eye closure and yawning, alerting users to prevent accidents caused by falling asleep at the wheel.

<div align="center">
  <img src="/api/placeholder/640/360" alt="Drowsiness Detection Demo">
</div>

## ✨ Features

- **Eye Closure Monitoring**: Detects when a driver's eyes remain closed for too long
- **Yawn Detection**: Identifies when the driver yawns, a sign of fatigue
- **Audio Alerts**: Plays warning sounds when drowsiness is detected
- **Activity Logging**: Records events for later analysis
- **Visual Interface**: Intuitive display showing metrics and warnings
- **Continuous Face Tracking**: Tracking algorithm maintains detection even with movement
- **Adjustable Thresholds**: Allows easy sensitivity customization of the system

## 💻 System Requirements

| Component | Minimum Requirements |
|------------|-------------------|
| Operating System | Windows (supported), Linux/Mac (requires sound alert modification) |
| CPU | 2.0 GHz dual-core |
| RAM | 4GB |
| Webcam | Camera with minimum 640x480 resolution |
| Python | 3.6 or higher |

## 📦 Installation

### 1. Install Dependencies

```bash
pip install opencv-python dlib numpy scipy argparse
```

### 2. Download the dlib Model

Download the `shape_predictor_68_face_landmarks.dat` file from the dlib website or official repository:

```bash
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
```

### 3. Verify Installation

Ensure all libraries are properly installed and the shape predictor file is placed in the same directory as the script or specified in the parameters.

## 🚀 Usage

### Run with Default Configuration:

```bash
python drowsiness_detector.py
```

### Run with Options:

```bash
python drowsiness_detector.py --shape-predictor path/to/shape_predictor_68_face_landmarks.dat --ear-threshold 0.25 --ear-frames 20 --yawn-threshold 0.6 --alarm --show-landmarks --log drowsiness_log.txt
```

## 🔧 How It Works

### System Architecture

<div align="center">
  <img src="/api/placeholder/700/300" alt="System Architecture">
</div>

### Processing Pipeline

1. **Image Acquisition**: Capture frames from webcam
2. **Face Detection**: Use dlib to locate faces
3. **Facial Landmark Extraction**: Identify 68 landmark points on the face
4. **Metric Calculation**:
   - Eye Aspect Ratio (EAR): Measures eye openness/closure
   - Mouth Ratio (MR): Measures mouth opening
5. **Decision Making**: Compare with thresholds and count consecutive frames
6. **Alert Triggering**: Activate warnings if thresholds are exceeded

### Calculation Formulas

#### Eye Aspect Ratio (EAR)

EAR is calculated based on the distances between facial landmark points of the eye:

<div align="center">
  <img src="/api/placeholder/400/150" alt="EAR Formula">
</div>

```
EAR = (||p₂-p₆|| + ||p₃-p₅||) / (2 * ||p₁-p₄||)
```

Where pᵢ are the facial landmark points of the eye.

#### Mouth Ratio (MR)

MR is calculated based on the ratio between the height and width of the mouth:

```
MR = ||p₁₃-p₁₉|| / ||p₀-p₆||
```

## ⚙️ Configuration Parameters

| Parameter | Description | Default Value |
|---------|-------|-----------------|
| `--shape-predictor` | Path to dlib facial landmark predictor file | `shape_predictor_68_face_landmarks.dat` |
| `--ear-threshold` | EAR threshold for detecting closed eyes | 0.25 |
| `--ear-frames` | Number of consecutive frames with EAR below threshold to trigger alert | 20 |
| `--yawn-threshold` | Mouth ratio threshold for yawn detection | 0.6 |
| `--camera` | Camera index | 0 |
| `--show-landmarks` | Display facial landmarks | False |
| `--alarm` | Enable audio alerts | False |
| `--log` | Path to log file | None |
| `--face-tracking` | Enable continuous face tracking | True |

## ⌨️ Keyboard Shortcuts

| Key | Function |
|------|-----------|
| `ESC` | Exit program |
| `r` | Reset counters |
| `+` | Increase EAR threshold |
| `-` | Decrease EAR threshold |

## 📝 Logging

When logging is enabled, the system records important events to a text file:

- Session start time
- Configuration parameters
- Yawn detection timestamps
- Drowsiness alert timestamps

Example log content:

```
==================================================
Drowsiness detection session started at 2025-05-09 15:30:45
EAR Threshold: 0.25, Frames: 20, Yawn Threshold: 0.6
==================================================

[2025-05-09 15:31:22] Detected yawn #1
[2025-05-09 15:32:45] ALERT: Drowsiness detected
[2025-05-09 15:35:10] Detected yawn #2
```

## 🔍 Troubleshooting

| Issue | Solution |
|--------|-----------|
| Face not detected | - Check lighting conditions<br>- Adjust camera position<br>- Ensure face is within frame |
| Inaccurate eye closure detection | - Adjust `--ear-threshold`<br>- Increase value for people with smaller eyes<br>- Decrease value for people with larger eyes |
| Alerts not triggering | - Check `--ear-frames` value<br>- Ensure `--alarm` is enabled |
| Slow performance | - Lower camera resolution<br>- Ensure hardware meets minimum requirements |
| Sound error | - For Linux/Mac, replace `winsound` module with equivalent solution |

## 👥 Contributing

Contributions to the project are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Future Development

- [ ] Cross-platform support for audio alerts
- [ ] Add head tilt detection capability
- [ ] Improve face tracking in low light conditions
- [ ] Develop a graphical user interface
- [ ] Integrate mobile device notifications

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.
