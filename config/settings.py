# settings.py
# Central configuration for the robotic chess player project

# Serial port for the MyCobot
ROBOT_COM_PORT = "COM8"         # It can depend based on your port

# Robot movement speed
ROBOT_SPEED = 60

# Step size for joint control (degrees)
JOINT_STEP = 5

# Camera index for OpenCV
CAMERA_INDEX = 0                # Usually 0 or 1, test your webcam

# OpenCV window settings
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 640
GRID_ROWS = 8
GRID_COLS = 8

# Gripper open/close values
GRIPPER_OPEN_VALUE = 100
GRIPPER_CLOSE_VALUE = 0
GRIPPER_SPEED = 70

# Safety Z offset for moves above squares
Z_RAISE_OFFSET = 30