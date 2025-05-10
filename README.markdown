# 😴 Real-time AI Face Detection Project

![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![Dlib](https://img.shields.io/badge/Dlib-19.x-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)
[![Stars](https://img.shields.io/github/stars/USERNAME/REPO_NAME?style=social)](https://github.com/USERNAME/REPO_NAME/stargazers)

A Python application leveraging OpenCV and Dlib for real-time monitoring of a user's eyes and mouth to detect signs of drowsiness, such as prolonged eye closure or frequent yawning. The system issues visual (including screen flashes) and audible alerts, making it ideal for applications like driver or machine operator fatigue monitoring.

---

## 🎞️ Live Demo

<!-- MODIFIED SECTION: Ensure these demos reflect the latest UI, especially the alarm toggle status and new alert behaviors -->
*Caption: Shows the initial interface with facial landmarks displayed, tracking the user's face in real-time. The runtime alarm status ('a' key) is shown at the bottom.*
![Demo 1](https://github.com/user-attachments/assets/7483ab68-3757-4b58-8fee-b946f25daec7) <!-- Replace with your updated image/GIF -->

*Caption: Demonstrates eye closure detection leading to a drowsiness alert, with screen flashing if the runtime alarm is active.*
![Demo 2](https://github.com/user-attachments/assets/f97d69e4-58da-41de-bc6d-03d59e960c9d) <!-- Replace with your updated image/GIF -->

*Caption: Highlights yawn detection. If the runtime alarm is active (via 'a' key), this can also trigger sound and screen flash.*
![Demo 3](https://github.com/user-attachments/assets/c3de3de2-a39d-48ca-8fc8-92d78799e2b2) <!-- Replace with your updated image/GIF -->

*Caption: Illustrates a triggered drowsiness alert with a visual warning, screen flash, and audible alarm in action (if runtime alarm is active).*
![Demo 4](https://github.com/user-attachments/assets/3cc87102-e383-4252-9137-6fdf810ac3e3) <!-- Replace with your updated image/GIF -->

---

## ✨ Key Features

<!-- MODIFIED SECTION -->
- **Eye Closure Detection:** Uses the Eye Aspect Ratio (EAR) algorithm to detect closed eyes.
- **Yawn Detection:** Calculates the Mouth Aspect Ratio (MAR) to identify yawning.
- **Real-time Alerts:**
  - Visual on-screen warnings and text.
  - **Dynamic Screen Flashing:** For drowsiness, and optionally for yawns if the runtime alarm is active.
  - **Toggleable Audible Alarms:** Sound alerts (Windows only, using `winsound`) can be turned ON/OFF during runtime with a hotkey.
- **Smart Face Tracking:** Attempts to re-acquire the face if it temporarily leaves the frame.
- **Facial Landmark Visualization:** Option to display 68 facial landmarks.
- **Event Logging:** Records session start, drowsiness, and yawning events to a log file (optional).
- **Flexible Configuration:**
  - Adjustable EAR, yawn thresholds, and frame counts via command-line arguments.
  - Runtime EAR threshold adjustment using hotkeys.
  - Runtime toggle for sound/event flash alarms.
- **Informative Display:**
  - Shows current time, session duration, EAR, MAR, PERCLOS, and yawn count.
  - Displays the status of the runtime alarm toggle.
- **Fullscreen Mode:** Toggleable with a hotkey.
- **Efficient Frame Processing:** Resizes frames for optimal performance.
- **PERCLOS Monitoring:** Calculates and displays the Percentage of Eye Closure over a configurable time window.

---

## 🛠️ Tech Stack

| Technology       | Description                                      |
|------------------|--------------------------------------------------|
| **Python 3.x**   | Core programming language.                       |
| **OpenCV**       | Image and video processing.                      |
| **Dlib**         | Face detection and facial landmark prediction.   |
| **NumPy**        | Array manipulation and numerical computing.      |
| **SciPy**        | Euclidean distance calculations.                 |
| **argparse**     | Command-line argument parsing.                   |
| **winsound**     | Sound alerts (Windows only).                     |
| **threading**    | Asynchronous sound alerts.                       |
| **collections**  | `deque` for efficient PERCLOS history.           |

---

## 📋 Prerequisites

Ensure the following requirements are met before starting:

1. **Python:** Version 3.7 or higher ([download](https://www.python.org/downloads/)).
2. **PIP:** Python's package installer (included with Python).
3. **Webcam:** A working webcam for video input.
4. **Dlib's Pre-trained Model:** Download `shape_predictor_68_face_landmarks.dat` from the [official Dlib website](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2).
   - Extract the `.bz2` file to obtain the `.dat` file. Place it in the project root or specify its path.

---

## ⚙️ Installation

1. **Clone the repository (replace `USERNAME/REPO_NAME`):**
   ```bash
   git clone https://github.com/USERNAME/REPO_NAME.git
   cd REPO_NAME
   ```

2. **Install required Python libraries:**
   It's recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

   Then install dependencies:
   ```bash
   pip install opencv-python dlib numpy scipy
   ```

   **Note:** Installing Dlib might require CMake and a C++ compiler.
   - On Ubuntu: `sudo apt-get update && sudo apt-get install build-essential cmake`
   - On Windows: You may need Visual Studio with C++ build tools. Often, installing cmake via pip first helps: `pip install cmake`, then `pip install dlib`.

3. **Place the Dlib model file:**
   Ensure `shape_predictor_68_face_landmarks.dat` is in the project's root directory or provide its path via the `--shape-predictor` argument.

---

## 🚀 Usage

Run the main Python script from your terminal:
```bash
python your_script_name.py [OPTIONS]
```
(Replace `your_script_name.py` with the actual name of your Python file).

### Command-line Arguments

<!-- MODIFIED SECTION -->
| Argument | Default Value | Description |
|----------|---------------|-------------|
| `--shape-predictor` | `shape_predictor_68_face_landmarks.dat` | Path to Dlib's facial landmark predictor file. |
| `--ear-threshold` | `0.23` | EAR threshold for detecting closed eyes. |
| `--ear-frames` | `25` | Consecutive frames below EAR threshold for drowsiness alert. |
| `--yawn-threshold` | `0.6` | Mouth Aspect Ratio (MAR) threshold for detecting a yawn. |
| `--camera` | `0` | Camera index (0 for primary webcam). |
| `--show-landmarks` | `False` | Display all 68 facial landmarks. |
| `--alarm` | `False` | Start with runtime sound/event flash alarm ON. (Toggled with 'a' key). |
| `--log` | `drowsiness_log.txt` | Path to log file (empty string '' disables logging). |
| `--face-tracking` | `True` | Enable face re-detection if temporarily lost. |
| `--perclos-window` | `60.0` | PERCLOS observation window in seconds. |

### Examples

Run with default settings (runtime alarm starts OFF unless `--alarm` is used):
```bash
python your_script_name.py
```

Start with runtime alarm ON, show landmarks, and use a custom log file:
```bash
python your_script_name.py --alarm --show-landmarks --log my_events.log
```

Use a secondary camera and a custom EAR threshold:
```bash
python your_script_name.py --camera 1 --ear-threshold 0.22
```

### Runtime Controls

<!-- MODIFIED SECTION -->
While the video window is active, use these keys:

| Key | Action |
|-----|--------|
| `ESC` | Exit the program. |
| `r` | Reset counters (eye blinks, yawns, PERCLOS) and alert states. |
| `+` | Increase EAR threshold by 0.01. |
| `-` | Decrease EAR threshold by 0.01 (min 0.01). |
| `f` | Toggle fullscreen mode. |
| `a` | Toggle runtime sound/event flash alarm ON/OFF. |

---

## 🔬 How It Works

1. **Initialization**: Loads the facial landmark model, initializes the webcam, and sets parameters including the initial state of the runtime alarm.
2. **Frame Acquisition & Preprocessing**: Captures frames, converts to grayscale, and resizes.
3. **Face Detection & Landmark Prediction**: Uses Dlib to find faces and predict 68 landmarks.
4. **Eye Aspect Ratio (EAR)**:
   - Calculated for both eyes. Formula: EAR = (|P2-P6| + |P3-P5|) / (2 * |P1-P4|).
   - If average EAR < ear_threshold, increments eye_blink_counter.
   - If eye_blink_counter ≥ ear_consec_frames, drowsiness_alert_visual_active is set to True.
5. **Mouth Aspect Ratio (MAR)**:
   - Calculated as MAR = Mouth_Height / Mouth_Width.
   - If MAR > yawn_threshold, a yawn event is registered, yawn_counter increments, and yawn_alert_visual_active is set True.
6. **PERCLOS (Percentage of Eye Closure)**:
   - Tracks eye closure status (based on EAR) over a defined time window (perclos_window_seconds).
   - Calculates PERCLOS = (time_eyes_closed_in_window / total_time_window) * 100%.
7. **Display**: Renders face bounding box, eye/mouth contours (optional: all landmarks), EAR, MAR, PERCLOS, time, session duration, yawn count, and alert status.
8. **Alerting**:
   - Visual Drowsiness Alert: Displays "DROWSINESS ALERT!" text and activates screen flashing (red).
   - Visual Yawn Alert: Displays "YAWN DETECTED!" text. If runtime_alarm_active is ON, also activates screen flashing (orange-ish).
   - Audible Alert: If runtime_alarm_active (toggled by 'a' key) is ON:
     - Plays a sound once per drowsiness episode.
     - Plays a sound once per yawn episode.
   - Terminal messages are printed for each detected drowsiness or yawn event, indicating if the runtime alarm was active.
9. **Logging**: Records session start, parameter values, yawn events, and drowsiness alerts with timestamps (if a log file path is provided).

---

## 📝 Logging

<!-- MODIFIED SECTION -->
When `--log <filename.txt>` is provided (default is `drowsiness_log.txt`), the script logs:

- Session start time, initial parameters, and initial runtime alarm state.
- Yawn events: `Yawn detected (Total: X, MAR: Y.YY)`
- Drowsiness alerts:
  - `ALERT: Drowsiness detected (EAR). Runtime alarm ON.` (if runtime alarm was ON)
  - `INFO: Drowsiness detected (EAR). Runtime alarm OFF.` (if runtime alarm was OFF)
- Yawn alerts when runtime alarm is active: `ALERT: Yawn detected. Runtime alarm ON.`
- Runtime alarm toggle events: `Runtime Sound/Event Flash Alarm Toggled: ON/OFF`

Example Log:
```
==================================================
Session started: 2024-05-11 10:00:00.123456
EAR Thresh: 0.23, EAR Frames: 25, Yawn Thresh: 0.6, PERCLOS Win: 60.0s
Initial Runtime Alarm (sound/event flash): OFF
==================================================

[2024-05-11 10:02:30] Runtime Sound/Event Flash Alarm Toggled: ON
[2024-05-11 10:05:15] Yawn detected (Total: 1, MAR: 0.75)
[2024-05-11 10:05:15] ALERT: Yawn detected. Runtime alarm ON.
[2024-05-11 10:10:30] ALERT: Drowsiness detected (EAR). Runtime alarm ON.
[2024-05-11 10:11:00] Runtime Sound/Event Flash Alarm Toggled: OFF
[2024-05-11 10:12:05] Yawn detected (Total: 2, MAR: 0.68)
[2024-05-11 10:15:45] INFO: Drowsiness detected (EAR). Runtime alarm OFF.
```

---

## 💡 Potential Future Enhancements

- Cross-platform audio alerts (e.g., using playsound or simpleaudio).
- Head pose estimation to detect nodding (a common drowsiness sign).
- More robust detection in challenging conditions (low light, glasses, partial face views).
- A graphical user interface (GUI) using Tkinter, PyQt, Kivy, or a web framework.
- Ability to save and load user-specific configuration profiles.
- Analysis of blink rate and duration as additional drowsiness indicators.
- Integration with other systems (e.g., sending alerts to a central monitoring system).

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit changes (`git commit -m 'Add AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file in the repository for details. If the file is missing, you can create one using a standard MIT License template (e.g., from choosealicense.com).

---

## ℹ️ Notes

- Remember to replace `USERNAME/REPO_NAME` with your actual GitHub username and repository name in badge URLs and clone commands if you fork this.
- Ensure your webcam drivers are up to date for best performance.
- The winsound library for audio alerts is Windows-specific. For other operating systems, consider alternatives mentioned in "Potential Future Enhancements."

Thank you for exploring this project!
