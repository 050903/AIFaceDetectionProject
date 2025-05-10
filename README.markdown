# 😴 Real-time AI Face Detection Project

![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![Dlib](https://img.shields.io/badge/Dlib-19.x-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)
[![Stars](https://img.shields.io/github/stars/USERNAME/REPO_NAME?style=social)](https://github.com/USERNAME/REPO_NAME/stargazers)

A Python application leveraging OpenCV and Dlib for real-time monitoring of a user's eyes and mouth to detect signs of drowsiness, such as prolonged eye closure or frequent yawning. The system issues visual and audible alerts, making it ideal for applications like driver or machine operator fatigue monitoring.

---

## 🎞️ Live Demo

![Demo 1](https://github.com/user-attachments/assets/7483ab68-3757-4b58-8fee-b946f25daec7)
![Demo 2](https://github.com/user-attachments/assets/f97d69e4-58da-41de-bc6d-03d59e960c9d)
![Demo 3](https://github.com/user-attachments/assets/c3de3de2-a39d-48ca-8fc8-92d78799e2b2)
![Demo 4](https://github.com/user-attachments/assets/3cc87102-e383-4252-9137-6fdf810ac3e3)

*Note:* Ensure these demo images or a GIF are uploaded to your repository or an image hosting service and update the URLs accordingly.

---

## ✨ Key Features

- **Eye Closure Detection:** Uses the Eye Aspect Ratio (EAR) algorithm to detect closed eyes.
- **Yawn Detection:** Calculates the Mouth Ratio (MR) to identify yawning.
- **Real-time Alerts:**
  - Visual on-screen warnings.
  - Optional audible alarms (Windows only, using `winsound`).
- **Smart Face Tracking:** Re-acquires the face if it leaves the frame.
- **Facial Landmark Visualization:** Option to display 68 facial landmarks.
- **Event Logging:** Records drowsiness and yawning events to a log file (optional).
- **Flexible Configuration:**
  - Adjustable EAR, yawn thresholds, and frame counts via command-line arguments.
  - Runtime EAR threshold adjustment using hotkeys.
- **Informative Display:**
  - Shows current time, session duration, EAR, MR, and yawn count.
  - Includes a progress bar for eye closure warnings.
- **Fullscreen Mode:** Toggleable with a hotkey.
- **Efficient Frame Processing:** Resizes frames for optimal performance.

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

---

## 📋 Prerequisites

Ensure the following requirements are met before starting:

1. **Python:** Version 3.7 or higher ([download](https://www.python.org/downloads/)).
2. **PIP:** Python's package installer (included with Python).
3. **Webcam:** A working webcam for video input.
4. **Dlib's Pre-trained Model:** Download `shape_predictor_68_face_landmarks.dat` from the [official Dlib website](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2).
   - Extract the `.bz2` file to obtain the `.dat` file.

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/USERNAME/REPO_NAME.git
   cd REPO_NAME
   ```

2. **Install required Python libraries:**
   The project includes a `requirements.txt` file listing all dependencies. Install them using:
   ```bash
   pip install -r requirements.txt
   ```
   *Note:* Installing Dlib on Linux or macOS may require `CMake` and a C++ compiler. For example, on Ubuntu:
   ```bash
   sudo apt-get update
   sudo apt-get install build-essential cmake
   ```
   On Windows, you may need Visual Studio with C++ build tools if Dlib installation fails.

3. **Verify the Dlib model file:**
   - Ensure the `shape_predictor_68_face_landmarks.dat` file is in the project's root directory (same folder as `main.py`). This file should already be included in the repository.

---

## 🚀 Usage

Run the main Python script (`main.py`) from your terminal:

```bash
python main.py [OPTIONS]
```

### Command-line Arguments

| Argument            | Default Value                          | Description                                              |
|---------------------|----------------------------------------|----------------------------------------------------------|
| `--shape-predictor` | `shape_predictor_68_face_landmarks.dat` | Path to Dlib's facial landmark predictor file.           |
| `--ear-threshold`   | `0.25`                                 | EAR threshold for detecting closed eyes.                 |
| `--ear-frames`      | `20`                                   | Consecutive frames below EAR threshold to trigger alarm. |
| `--yawn-threshold`  | `0.6`                                  | Mouth Ratio threshold for detecting a yawn.              |
| `--camera`          | `0`                                    | Camera index (0 for primary webcam).                     |
| `--show-landmarks`  | `False`                                | Display 68 facial landmarks.                             |
| `--alarm`           | `False`                                | Enable sound alarm for drowsiness detection.             |
| `--log`             | `''` (empty)                           | Path to log file (empty disables logging).               |
| `--face-tracking`   | `True`                                 | Enable face re-detection if lost.                        |

### Examples

- Run with default settings:
  ```bash
  python main.py
  ```

- Enable sound alarm, landmarks, and logging:
  ```bash
  python main.py --alarm --show-landmarks --log events.log
  ```

- Use a secondary camera and a custom EAR threshold:
  ```bash
  python main.py --camera 1 --ear-threshold 0.22
  ```

### Runtime Controls

While the video window is active, use these keys:

| Key | Action                                    |
|-----|-------------------------------------------|
| `ESC` | Exit the program.                       |
| `r`   | Reset eye closure and yawn counters.     |
| `+`   | Increase EAR threshold by 0.01.          |
| `-`   | Decrease EAR threshold by 0.01 (min 0.01). |
| `f`   | Toggle fullscreen mode.                  |

---

## 🔬 How It Works

1. **Initialization:** Loads the facial landmark model, initializes the webcam, and sets parameters.
2. **Frame Acquisition:** Captures frames from the webcam.
3. **Preprocessing:** Converts frames to grayscale and resizes them for efficiency.
4. **Face Detection:** Uses `dlib.get_frontal_face_detector()` to locate faces.
5. **Facial Landmark Prediction:** Applies `dlib.shape_predictor()` to identify 68 facial landmarks (eyes, nose, mouth, jawline).
6. **Eye Aspect Ratio (EAR):**
   - Calculates EAR for both eyes using Euclidean distances between landmarks.
   - Formula: `EAR = (A + B) / (2.0 * C)` (see `eye_aspect_ratio` function).
   - If average EAR < `ear_threshold`, increments `eye_counter`.
   - If `eye_counter` ≥ `ear_consec_frames`, triggers a drowsiness alert.
7. **Mouth Ratio (MR):**
   - Computes MR based on vertical and horizontal mouth landmark distances.
   - Formula: `MR = Mouth_Height / Mouth_Width` (see `mouth_ratio` function).
   - If MR > `yawn_threshold`, increments `yawn_count`.
8. **Display:** Renders eye/mouth contours, EAR, MR, time, alerts, and progress bars.
9. **Alerting:** Shows visual alerts and plays audio (if enabled) for drowsiness.
10. **Logging:** Records session start, yawns, and alerts with timestamps (if enabled).

---

## 📝 Logging

When `--log <filename.txt>` is provided, the script logs:

- Session start time and threshold values.
- Yawn events (`Yawn detected - count X`).
- Drowsiness alerts (`ALERT: Drowsiness detected`).

**Example Log:**
```
==================================================
Drowsiness detection session started at 2023-10-27 10:00:00
EAR Threshold: 0.25, Frames: 20, Yawn Threshold: 0.6
==================================================

[2023-10-27 10:05:15] Yawn detected - count 1
[2023-10-27 10:10:30] ALERT: Drowsiness detected
[2023-10-27 10:12:05] Yawn detected - count 2
```

---

## 💡 Potential Future Enhancements

- Cross-platform audio alerts (e.g., using `playsound` for Linux/macOS).
- Head pose estimation to detect nodding.
- Improved accuracy in low-light or with glasses.
- User-friendly GUI (e.g., Tkinter, PyQt, or Kivy).
- Save/load user configurations.
- Blink rate analysis.

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

This project is licensed under the MIT License. See the `LICENSE` file in the repository for details. If the file is missing, create one using the standard MIT License template.

---

## ℹ️ Notes

- Replace `USERNAME/REPO_NAME` with your GitHub username and repository name in badge URLs and clone commands.
- Test the script thoroughly to ensure compatibility with your system and webcam.
- For demo images/GIFs, upload them to your repository or an image hosting service and update the URLs in the "Live Demo" section.

Thank you for exploring this project! We hope it proves useful and inspires further innovation.