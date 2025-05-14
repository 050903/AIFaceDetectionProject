# 😴 Real-time AI Face Detection Project

![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![Dlib](https://img.shields.io/badge/Dlib-19.x-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)
[![Stars](https://img.shields.io/github/stars/USERNAME/REPO_NAME?style=social)](https://github.com/USERNAME/REPO_NAME/stargazers)

A Python application leveraging OpenCV and Dlib for real-time monitoring of a user's eyes and mouth to detect signs of drowsiness, such as prolonged eye closure or frequent yawning. The system issues visual (including screen flashes) and audible alerts, making it ideal for applications like driver or machine operator fatigue monitoring.

---

## 🎞️ Live Demo


### Project Initialization (Terminal Output)

![Start terminal](https://github.com/user-attachments/assets/45d21a7c-1e43-4e95-9832-eb2e39c392d4)

This image shows the terminal when the program is first launched. It displays usage instructions including keyboard shortcuts: ESC to exit, 'r' to reset counters, '+/-' to adjust EAR threshold, 'f' to toggle fullscreen, and 'a' to toggle the sound/flash alarm. The initial sound/flash alarm state is OFF, and we can see system messages indicating the program is loading the facial landmark predictor, initializing the camera, and starting drowsiness detection.

### No Face Detected State

![No face detected screen](https://github.com/user-attachments/assets/ba235fe3-98e7-42fe-a728-c8ce49e87681)

This screen shows when no face is in the frame. The interface displays "NO FACE DETECTED" in red. The current time is 20:14:16 with an elapsed session time of 00:01:25.2. EAR and MAR values are "N/A" since there's no face to measure. PERCLOS shows 17.5%, indicating some eye closure was detected in the previous minute. The yawn counter remains at 0, and the alarm status is OFF.

### Face Detection Searching Phase

![Searching face screen](https://github.com/user-attachments/assets/068f6250-c63e-4ef2-86e6-3d1e4231174b)

The interface shows the Drowsiness Detection System in its searching phase, attempting to locate a face in the webcam feed. The top left shows the current time (20:13:35), and the top right shows elapsed session time (00:00:44.0). The system displays "SEARCHING..." in red, indicating it's trying to detect a face. EAR and MAR values show "N/A" since no face is fully detected yet. The PERCLOS value is 11.6% for the 60-second window. The yawn counter shows 0, and the alarm key status ('a') is OFF.

 ### Simultaneous Drowsiness and Yawn Detection
 
 ![Yawn detected](https://github.com/user-attachments/assets/e66ffdd3-3fdf-4c55-a916-a2512cce1c49)

This screenshot shows both a drowsiness alert and yawn detection occurring simultaneously. The current time is 20:16:13 with a session duration of 00:03:22.5. The EAR value is 0.19 (below the default threshold of 0.23), and the MAR value is 0.71 (above the yawn threshold of 0.6). PERCLOS is extremely high at 77.1%, indicating significant eye closure in the past minute. The system displays both "DROWSINESS ALERT!" in red and "YAWN DETECTED!" in orange. The face is highlighted with a green box, with eye contours (green) and mouth contour (blue) visible. The yawn counter shows 84, and the alarm is OFF.


### Active Drowsiness Detection

![Drowsiness alert](https://github.com/user-attachments/assets/d8c6fe4a-5b1f-43eb-bdf5-48b884149b9c)

The final image shows a clear drowsiness alert at 20:16:36. The EAR value is very low at 0.13, indicating significantly closed eyes. The MAR value is 0.04, showing a closed mouth. PERCLOS remains high at 73.8%. "DROWSINESS ALERT!" is prominently displayed in red. The face is again highlighted with a green box showing the facial landmarks, with nearly closed eyes (green contours) and closed mouth (blue contour). The yawn counter shows 86, indicating continued monitoring from the previous state.


### Console Log Showing Yawn Detection Events

![Report event detected](https://github.com/user-attachments/assets/a8335235-49cb-4519-9699-c7b5a2babc2e)

The console output shows a series of yawn detection events. Starting at 20:26:16, the system detected 7 yawns over a short period, with MAR values ranging from 0.60 to 0.66. At 20:26:19, the runtime sound/flash alarm was toggled ON, and subsequent yawn detections (from number 5 onward) generated "ALERT" messages with "Runtime alarm active" notifications, indicating that both visual and sound alerts were triggered.

## Video project 

### ---> Click to open
[![Watch the video](https://img.youtube.com/vi/nR_KZxuanC4/hqdefault.jpg)](https://youtu.be/nR_KZxuanC4)

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

## 👨‍💻 Author
Trần Thế Hảo

# 🎓 Information Technology, University of Transport Ho Chi Minh City (UTH)

![image](https://github.com/user-attachments/assets/c2488ba6-05d8-40dd-b8c6-ff3db7cf8cf5)
