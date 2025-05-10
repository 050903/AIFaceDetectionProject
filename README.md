😴 Real-time AI Face Detection Project

A Python application leveraging OpenCV and Dlib for real-time monitoring of a user's eyes and mouth to detect signs of drowsiness, such as prolonged eye closure or frequent yawning. The system issues visual and audible alerts, making it ideal for applications like driver or machine operator fatigue monitoring.

🎞️ Live Demo

Note: Ensure these demo images or a GIF are uploaded to your repository or an image hosting service and update the URLs accordingly.

✨ Key Features

Eye Closure Detection: Uses the Eye Aspect Ratio (EAR) algorithm to detect closed eyes.
Yawn Detection: Calculates the Mouth Ratio (MR) to identify yawning.
Real-time Alerts:
Visual on-screen warnings.
Optional audible alarms (Windows only, using winsound).


Smart Face Tracking: Re-acquires the face if it leaves the frame.
Facial Landmark Visualization: Option to display 68 facial landmarks.
Event Logging: Records drowsiness and yawning events to a log file (optional).
Flexible Configuration:
Adjustable EAR, yawn thresholds, and frame counts via command-line arguments.
Runtime EAR threshold adjustment using hotkeys.


Informative Display:
Shows current time, session duration, EAR, MR, and yawn count.
Includes a progress bar for eye closure warnings.


Fullscreen Mode: Toggleable with a hotkey.
Efficient Frame Processing: Resizes frames for optimal performance.


🛠️ Tech Stack



Technology
Description



Python 3.x
Core programming language.


OpenCV
Image and video processing.


Dlib
Face detection and facial landmark prediction.


NumPy
Array manipulation and numerical computing.


SciPy
Euclidean distance calculations.


argparse
Command-line argument parsing.


winsound
Sound alerts (Windows only).


threading
Asynchronous sound alerts.



📋 Prerequisites
Ensure the following requirements are met before starting:

Python: Version 3.7 or higher (download).
PIP: Python's package installer (included with Python).
Webcam: A working webcam for video input.
Dlib's Pre-trained Model: Download shape_predictor_68_face_landmarks.dat from the official Dlib website.
Extract the .bz2 file to obtain the .dat file.




⚙️ Installation

Clone the repository:
git clone https://github.com/USERNAME/REPO_NAME.git
cd REPO_NAME


Install required Python libraries:The project includes a requirements.txt file listing all dependencies. Install them using:
pip install -r requirements.txt

Note: Installing Dlib on Linux or macOS may require CMake and a C++ compiler. For example, on Ubuntu:
sudo apt-get update
sudo apt-get install build-essential cmake

On Windows, you may need Visual Studio with C++ build tools if Dlib installation fails.

Verify the Dlib model file:

Ensure the shape_predictor_68_face_landmarks.dat file is in the project's root directory (same folder as main.py). This file should already be included in the repository.




🚀 Usage
Run the main Python script (main.py) from your terminal:
python main.py [OPTIONS]

Command-line Arguments



Argument
Default Value
Description



--shape-predictor
shape_predictor_68_face_landmarks.dat
Path to Dlib's facial landmark predictor file.


--ear-threshold
0.25
EAR threshold for detecting closed eyes.


--ear-frames
20
Consecutive frames below EAR threshold to trigger alarm.


--yawn-threshold
0.6
Mouth Ratio threshold for detecting a yawn.


--camera
0
Camera index (0 for primary webcam).


--show-landmarks
False
Display 68 facial landmarks.


--alarm
False
Enable sound alarm for drowsiness detection.


--log
'' (empty)
Path to log file (empty disables logging).


--face-tracking
True
Enable face re-detection if lost.


Examples

Run with default settings:
python main.py


Enable sound alarm, landmarks, and logging:
python main.py --alarm --show-landmarks --log events.log


Use a secondary camera and a custom EAR threshold:
python main.py --camera 1 --ear-threshold 0.22



Runtime Controls
While the video window is active, use these keys:



Key
Action



ESC
Exit the program.


r
Reset eye closure and yawn counters.


+
Increase EAR threshold by 0.01.


-
Decrease EAR threshold by 0.01 (min 0.01).


f
Toggle fullscreen mode.



🔬 How It Works

Initialization: Loads the facial landmark model, initializes the webcam, and sets parameters.
Frame Acquisition: Captures frames from the webcam.
Preprocessing: Converts frames to grayscale and resizes them for efficiency.
Face Detection: Uses dlib.get_frontal_face_detector() to locate faces.
Facial Landmark Prediction: Applies dlib.shape_predictor() to identify 68 facial landmarks (eyes, nose, mouth, jawline).
Eye Aspect Ratio (EAR):
Calculates EAR for both eyes using Euclidean distances between landmarks.
Formula: EAR = (A + B) / (2.0 * C) (see eye_aspect_ratio function).
If average EAR < ear_threshold, increments eye_counter.
If eye_counter ≥ ear_consec_frames, triggers a drowsiness alert.


Mouth Ratio (MR):
Computes MR based on vertical and horizontal mouth landmark distances.
Formula: MR = Mouth_Height / Mouth_Width (see mouth_ratio function).
If MR > yawn_threshold, increments yawn_count.


Display: Renders eye/mouth contours, EAR, MR, time, alerts, and progress bars.
Alerting: Shows visual alerts and plays audio (if enabled) for drowsiness.
Logging: Records session start, yawns, and alerts with timestamps (if enabled).


📝 Logging
When --log <filename.txt> is provided, the script logs:

Session start time and threshold values.
Yawn events (Yawn detected - count X).
Drowsiness alerts (ALERT: Drowsiness detected).

Example Log:
==================================================
Drowsiness detection session started at 2023-10-27 10:00:00
EAR Threshold: 0.25, Frames: 20, Yawn Threshold: 0.6
==================================================

[2023-10-27 10:05:15] Yawn detected - count 1
[2023-10-27 10:10:30] ALERT: Drowsiness detected
[2023-10-27 10:12:05] Yawn detected - count 2


💡 Potential Future Enhancements

Cross-platform audio alerts (e.g., using playsound for Linux/macOS).
Head pose estimation to detect nodding.
Improved accuracy in low-light or with glasses.
User-friendly GUI (e.g., Tkinter, PyQt, or Kivy).
Save/load user configurations.
Blink rate analysis.


🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/AmazingFeature).
Commit changes (git commit -m 'Add AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a Pull Request.


📜 License
This project is licensed under the MIT License. See the LICENSE file in the repository for details. If the file is missing, create one using the standard MIT License template.

ℹ️ Notes

Replace USERNAME/REPO_NAME with your GitHub username and repository name in badge URLs and clone commands.
Test the script thoroughly to ensure compatibility with your system and webcam.
For demo images/GIFs, upload them to your repository or an image hosting service and update the URLs in the "Live Demo" section.

Thank you for exploring this project! We hope it proves useful and inspires further innovation.
