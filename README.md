# EyeAssist – AI-Based Facial Gesture and Voice Control System


## 📌 Overview

EyeAssist is an AI-powered assistive technology system that allows users to control a computer using eye movements, eye blinks, and voice commands.

The system uses computer vision, facial landmarks, machine learning, and voice recognition to provide hands-free computer interaction.

## 🎯 Objectives

- Enable hands-free computer control.
- Control the mouse using eye movements and blinks.
- Recognize eye gestures using a machine learning model.
- Provide voice-based computer control.
- Improve accessibility for users who have difficulty using a traditional mouse and keyboard.
- Provide a simple dashboard to control and monitor the system.

## ✨ Key Features

### 👁️ Eye Control

- Eye movement-based cursor control.
- Left eye blink → Left click.
- Right eye blink → Right click.
- Both eyes blink → Double click.
- Look left, right, up, and down gesture recognition.
- Automatic eye calibration.
- Cursor smoothing for better control.
- Pause and resume eye control.
- Automatic safety pause when no face is detected.
- Automatic recalibration when a new user is detected.

### 🎙️ Voice Control

- Voice-based mouse control.
- Left click.
- Right click.
- Double click.
- Scroll up and down.
- Press keyboard keys using voice commands.
- Type text using voice.
- Open websites and applications using voice commands.
- Search files and information using voice commands.
- Minimize, maximize, and close windows using voice commands.

### 🤖 AI Model

EyeAssist uses a Random Forest Classifier to recognize eye gestures from extracted eye and gaze features.

## 🧠 Machine Learning Details

- Algorithm: Random Forest Classifier
- Number of Features: 10
- Training Samples: 2125
- Test Accuracy: 92.47%

### Extracted Features

- Left Eye Aspect Ratio (EAR)
- Right Eye Aspect Ratio (EAR)
- Iris X position
- Iris Y position
- Gaze X position
- Gaze Y position
- Left eye horizontal ratio
- Right eye horizontal ratio
- Left eye vertical ratio
- Right eye vertical ratio

### Recognized Gestures

- Normal
- Left Blink
- Right Blink
- Both Blink
- Look Left
- Look Right
- Look Up
- Look Down

## 🔄 System Pipeline

```text
Laptop Camera
      ↓
    OpenCV
      ↓
   MediaPipe
      ↓
Face & Eye Landmarks
      ↓
 Feature Extraction
      ↓
 Random Forest Model
      ↓
  Eye Gesture
      ↓
Mouse / Keyboard Control

## 🛠️ Technology Stack

### Programming Language
- Python 3.12

### Computer Vision
- OpenCV
- MediaPipe

### Machine Learning
- NumPy
- Pandas
- Scikit-learn
- Random Forest Classifier

### Computer Control
- PyAutoGUI

### Voice Control
- SpeechRecognition
- PyAudio

### User Interface
- Tkinter

### Development Tools
- Visual Studio Code
- Git
- GitHub

## 📂 Project Structure

```text
eyeaassit/
│
├── dashboard.py
├── ai_mouse_control.py
├── voice_control.py
├── eye_detection.py
├── gaze_test.py
├── collect_data.py
├── train_model.py
├── test_model.py
├── camera_test.py
├── eye_gesture_data.csv
├── eye_gesture_model.pkl
├── requirements.txt
└── README.md

## 💻 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd eyeaassit
```

### 2. Create a Virtual Environment

Python 3.12 is recommended.

```bash
py -3.12 -m venv venv
```

### 3. Activate the Virtual Environment

On Windows:

```bash
.\venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Project

Start the main dashboard:

```bash
python dashboard.py
```

The dashboard allows you to start and control the Eye Control and Voice Control systems.

## 🖱️ Eye Gesture Controls

| Eye Gesture     | Action                  |
| --------------- | ----------------------- |
| Left Blink      | Left Click              |
| Right Blink     | Right Click             |
| Both Eyes Blink | Double Click            |
| Look Left       | Eye Gesture Recognition |
| Look Right      | Eye Gesture Recognition |
| Look Up         | Eye Gesture Recognition |
| Look Down       | Eye Gesture Recognition |
| P               | Pause / Resume          |
| Q               | Exit                    |

## 🔐 Safety Features

* The system pauses when no face is detected.
* A short delay prevents temporary camera detection loss from immediately interrupting the system.
* New users are automatically calibrated.
* Eye control can be manually paused.
* Cursor movement is smoothed to reduce sudden movements.

## 📊 Dashboard

The EyeAssist dashboard provides a centralized interface for:

* Eye Control
* Voice Control
* AI Model information
* System status
* Camera status
* Model status

## 🎯 Use Cases

EyeAssist can be useful for:

* Hands-free computer interaction.
* Accessibility applications.
* Assistive technology.
* Human-computer interaction research.
* AI and computer vision demonstrations.
* Educational AI/ML projects.

## 🚀 Future Improvements

* Improve eye gesture recognition accuracy.
* Add personalized user calibration.
* Improve cursor movement accuracy.
* Add more voice commands.
* Improve performance in different lighting conditions.
* Support more assistive computer-control features.
* Develop a more advanced accessibility interface.

## ⚠️ Limitations

* Performance depends on camera quality.
* Lighting conditions can affect eye and face detection.
* Eye gesture recognition may vary between users.
* Voice commands require a working microphone.
* PyAudio setup may vary depending on the operating system.

## 📦 Requirements

All required Python packages are listed in:

```text
requirements.txt
```

## 👩‍💻 Project Information

**Project Name:** EyeAssist – AI-Based Eye Control System

**Domain:** Artificial Intelligence, Machine Learning, Computer Vision and Assistive Technology

**Programming Language:** Python

## 📄 License

This project is developed for educational and project demonstration purposes.
