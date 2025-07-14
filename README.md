Purdue-Cobot/  
│  
├── app.py  
├── detect_move.py  
├── functions.py  
├── requirements.txt  
├── README.md  
│  
├── config/  
│   ├── settings.py  
│   └── squares.py  
│  
├── robot/  
│   ├── arm_control.py  
│   └── __init__.py  
│
└── vision/  
    ├── camera_grid.py  
    └── __init__.py  
📜 Description of Folders and Files  
✅ Top-level files  
# app.py  
Main GUI launcher using Tkinter. Lets user choose control modes like keyboard control, playing with the robot, or editing square coordinates.

# detect_move.py
Opens camera, overlays chess grid, lets user click squares to move the robot there.

# functions.py
Core robot movement and gripper control utilities, including home positioning and pick-and-place logic.

# requirements.txt
Lists Python dependencies:

- Copy
- Edit
- opencv-python
- python-chess
- pymycobot

# ✅ config/ Folder
settings.py
Stores global settings like COM port, speed, camera index.

## squares.py
Python dictionary mapping chess squares (e.g. 'e4') to robot coordinates [X, Y, Z, Rx, Ry, Rz]. User-editable for calibration.

✅ Purpose: Central place for configuration and calibration data.

# ✅ robot/ Folder
## arm_control.py  
Low-level robot API to:

Move joints

Open/close gripper

Return to home position

Provide keyboard control with camera view

## __init__.py
Makes this folder an importable package.

✅ Purpose: Encapsulates all MyCobot hardware communication.

# ✅ vision/ Folder
camera_grid.py
Opens live camera feed with an overlaid chess grid. Lets user click on squares to send robot to those positions.

## __init__.py
Makes this folder an importable package.

✅ Purpose: Contains all camera-related utilities.

# ✅ 🔗 How It All Fits Together
## app.py is the entry point. It:

Shows a GUI with multiple buttons.

Calls functions in robot/arm_control.py for movement and gripper control.

Calls vision/camera_grid.py to show the camera feed with chess grid overlay.

Reads/writes chess-square coordinates in config/squares.py.

detect_move.py is a standalone test:

Runs the camera + grid overlay.

Lets the user click a square to move the robot there.

## functions.py:

Provides reusable movement helpers.

Used in both the app and other scripts.

# ✅ 🔧 How to Install & Run
## 1️⃣ Install dependencies  
pip install -r requirements.txt
## 2️⃣ Launch the GUI
python app.py


✅ You’ll see options for:

### Keyboard Control

### Play with the Robot

### Play Against the Robot

### Edit Square Coordinates

## ✅ 🎛️ Editing Square Coordinates
✔️ Click "Edit Square Coordinates" in the app:

Opens a window listing all squares (like e4).

Lets you edit their X, Y, Z, Rx, Ry, Rz values.

Saves them back to config/squares.py.

✅ Perfect for calibration with your physical chess board.

✅ ⚙️ Example of Keyboard Control
✔️ In the Keyboard Control window:

z / x → Joint 1

c / v → Joint 2

q / a → Joint 3

w / s → Joint 4

e / d → Joint 5

r / f → Joint 6

o → Toggle gripper

h → Return home

p → Print coordinates

ESC → Exit

✅ Includes live camera feed with grid overlay for visual feedback.

✅ 📌 Design Philosophy
Separation of concerns:

### config/: All settings and calibration data.

### robot/: All robot-specific movement logic.

### vision/: Camera-based grid interaction.

Top-level scripts to launch GUIs and demos.

User friendly:

GUI to choose modes.

Built-in coordinate editor.

Visual grid overlay for move planning.

# ✅ 🚀 Author
Built by **ABD DAHAR MAHMOUD LEGHLIMI**
For research and development using MyCobot 320.
