# 😴 Real-time Drowsiness Detection System

![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![Dlib](https.img.shields.io/badge/Dlib-19.x-orange)
![License](https.img.shields.io/badge/License-MIT-brightgreen)
[![Stars](https://img.shields.io/github/stars/your-username/your-repo-name?style=social)](https://github.com/your-username/your-repo-name/stargazers) <!-- Replace your-username/your-repo-name -->

A Python application leveraging OpenCV and Dlib to monitor a user's eyes and mouth in real-time. It detects signs of drowsiness, such as prolonged eye closure or frequent yawning, and issues alerts. This system is particularly useful for warning drivers or machine operators when they show signs of fatigue.

---

## 🎞️ Live Demo / How it Looks

![Demo GIF](https://user-images.githubusercontent.com/your-github-id/your-repo-id/path-to-your-demo.gif)
*<p align="center">Main interface of the system in action (replace with your actual GIF/image)</p>*

---

## ✨ Key Features

*   **Eye Closure Detection:** Utilizes the Eye Aspect Ratio (EAR) algorithm to determine eye state.
*   **Yawn Detection:** Calculates Mouth Ratio (MR) to identify yawning behavior.
*   **Real-time Alerts:**
    *   Visual on-screen warnings.
    *   Audible alarms (optional, uses `winsound` for Windows).
*   **Smart Face Tracking:** Attempts to re-acquire the face if it's lost from the frame.
*   **Facial Landmark Visualization:** Option to display 68 facial landmarks.
*   **Event Logging:** Saves drowsiness and yawning events to a log file (optional).
*   **Flexible Configuration:**
    *   Adjust thresholds (EAR, yawn) and consecutive frame counts via command-line arguments.
    *   Runtime EAR threshold adjustment using hotkeys.
*   **Informative Display:**
    *   Displays current time and session elapsed time.
    *   Shows current EAR and MR values.
    *   Progress bar for eye closure warning.
    *   Yawn counter.
*   **Fullscreen Mode:** Easily toggleable with a hotkey.
*   **Efficient Frame Processing:** Resizes frames for processing and display.

---

## 🛠️ Tech Stack

| Technology      | Description                                      |
|-----------------|--------------------------------------------------|
| **Python 3.x**  | Primary programming language.                    |
| **OpenCV**      | Image and video processing library.              |
| **Dlib**        | Face detection and facial landmark prediction.   |
| **NumPy**       | Numerical computing, array manipulation.         |
| **SciPy**       | Euclidean distance calculation.                  |
| **argparse**    | Command-line argument parsing.                   |
| **winsound**    | Plays sound alerts (Windows only).               |
| **threading**   | Runs sound alerts asynchronously.                |

---

## 📋 Prerequisites

Before you begin, ensure you have met the following requirements:

1.  **Python:** Version 3.7 or higher.
2.  **PIP:** Python's package installer.
3.  **Webcam:** For video input.
4.  **Dlib's pre-trained model `shape_predictor_68_face_landmarks.dat`.**
    *   You can download it from the [official Dlib website](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2).
    *   Extract the `.bz2` file after downloading to get the `.dat` file.

---

## ⚙️ Installation

1.  **Clone the repository (or download the source code):**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git # Replace with your repo URL
    cd your-repo-name
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install opencv-python dlib numpy scipy
    ```
    *Note:* On some systems (especially Linux or macOS), installing Dlib might require `CMake` and a C++ compiler to be installed first. Refer to the Dlib documentation for details.
    ```bash
    # Example for installing CMake on Ubuntu
    # sudo apt-get update
    # sudo apt-get install build-essential cmake
    ```

3.  **Place the `shape_predictor_68_face_landmarks.dat` file:**
    *   Copy the `shape_predictor_68_face_landmarks.dat` file (downloaded and extracted in the "Prerequisites" step) into the project's root directory (the same directory as your main Python script, e.g., `drowsiness_detector.py`).

---

## 🚀 Usage

Run the main Python script (e.g., `drowsiness_detector.py`) from your terminal:

```bash
python drowsiness_detector.py [OPTIONS]
Use code with caution.
Markdown
Command-line Arguments:
Argument	Default Value	Description
--shape-predictor	shape_predictor_68_face_landmarks.dat	Path to the Dlib facial landmark predictor file.
--ear-threshold	0.25	Eye Aspect Ratio (EAR) threshold for detecting closed eyes.
--ear-frames	20	Number of consecutive frames with EAR below threshold to trigger an alarm.
--yawn-threshold	0.6	Mouth Ratio (MR) threshold for detecting a yawn.
--camera	0	Camera index (default is 0 for the primary/built-in webcam).
--show-landmarks	False (not active)	Flag to display the 68 facial landmarks on the face.
--alarm	False (not active)	Flag to enable sound alarm on drowsiness detection.
--log	'' (empty string)	Path to the log file. If empty, logging is disabled.
--face-tracking	True (active)	Flag to enable continuous face tracking and re-detection if face is lost.
Examples:
Run with default settings:
python drowsiness_detector.py
Use code with caution.
Bash
Run with sound alarm, landmark display, and logging:
python drowsiness_detector.py --alarm --show-landmarks --log events.log
Use code with caution.
Bash
Run with a secondary camera and a custom EAR threshold:
python drowsiness_detector.py --camera 1 --ear-threshold 0.22
Use code with caution.
Bash
⌨️ Runtime Controls
While the video window is active, you can use the following keys:
Key	Action
ESC	Exit the program.
r	Reset eye closure counter (eye_counter) and yawn count (yawn_count).
+	Increase EAR threshold (ear_threshold) by 0.01.
-	Decrease EAR threshold (ear_threshold) by 0.01 (minimum 0.01).
f	Toggle fullscreen mode.
🔬 How It Works (Overview)
Initialization: Loads the facial landmark model, initializes the camera, and sets parameters.
Frame Acquisition: Reads frames one by one from the webcam.
Preprocessing: Converts the frame to grayscale and resizes it (if necessary).
Face Detection: Uses dlib.get_frontal_face_detector() to find faces in the grayscale image.
Facial Landmark Prediction: For each detected face, dlib.shape_predictor() localizes 68 specific points (eyes, nose, mouth, jawline).
Calculate Eye Aspect Ratio (EAR):
EAR is computed for both eyes based on Euclidean distances between vertical and horizontal eye landmarks.
Formula: EAR = (A + B) / (2.0 * C) (see eye_aspect_ratio function).
The average EAR of both eyes is used.
If avg_ear < ear_threshold, the eye_counter increments.
If eye_counter >= ear_consec_frames, a drowsiness alert is triggered.
Calculate Mouth Ratio (MR):
MR is calculated based on the vertical and horizontal distances of landmarks around the mouth.
Formula: MR = Mouth_Height / Mouth_Width (see mouth_ratio function).
If mr > yawn_threshold, a yawn is registered (yawn_count increments).
Display Information: Draws contours around eyes and mouth, displays EAR, MR, time, alerts, and progress bars on the frame.
Alerting: If drowsiness is detected, a prominent visual alert is displayed, and an audio alarm is played (if --alarm flag is enabled).
Logging: If a log file path is provided, events like session start, yawns, and drowsiness alerts are recorded with timestamps.
📝 Logging
If the --log <filename.txt> argument is provided when running the script, a log file will be created (or appended to if it already exists) with the following information:
Timestamp of when the drowsiness detection session started.
The threshold values (EAR, frames, yawn) used for the session.
Timestamp and event for "Yawn detected - count X".
Timestamp and event for "ALERT: Drowsiness detected".
Example Log Snippet:
==================================================
Drowsiness detection session started at 2023-10-27 10:00:00
EAR Threshold: 0.25, Frames: 20, Yawn Threshold: 0.6
==================================================

[2023-10-27 10:05:15] Yawn detected - count 1
[2023-10-27 10:10:30] ALERT: Drowsiness detected
[2023-10-27 10:12:05] Yawn detected - count 2
Use code with caution.
💡 Potential Future Enhancements
Cross-platform sound alerts (Linux/macOS using playsound or similar).
Integrate head pose estimation to detect nodding.
Improve accuracy in low-light conditions or when the user is wearing glasses.
Develop a more user-friendly Graphical User Interface (GUI) using Tkinter, PyQt, or Kivy.
Implement user configuration saving/loading.
Analyze blink rate.
🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.
Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
📜 License
This project is licensed under the MIT License. See the LICENSE file (if available) for more details.
Thank you for your interest in this project! We hope you find it useful.
**Important Reminders:**

1.  **`your-username/your-repo-name`:** Replace these placeholders with your actual GitHub username and repository name for the badges and links to work correctly.
2.  **`drowsiness_detector.py`:** Replace this with the actual name of your main Python script if it's different.
3.  **Live Demo (GIF/Image):** Create a short GIF or take a screenshot of your program in action and add it to the "Live Demo" section. Upload the image/GIF to a GitHub issue or an image hosting service and use its link.
4.  **`LICENSE` File:** If you choose the MIT license, create a file named `LICENSE` in your project's root directory and paste the MIT license text into it. You can easily find MIT license templates online.
5.  **Update as Needed:** Adjust any information (library versions, features, etc.) to accurately reflect your project.
