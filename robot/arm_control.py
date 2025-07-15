# Connects to robot arm and includes functions to move to home position and send coordinates.
import time
from pymycobot import MyCobot320
from config import settings
from pynput import keyboard
import cv2

# Function to connect to the MyCobot320 robot arm
def connect_robot():
    print(f"Connecting to MyCobot on {settings.ROBOT_COM_PORT}...")
    try:
        mc = MyCobot320(settings.ROBOT_COM_PORT, 115200)
        return mc
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

# Function to move the robot arm to the home position
def move_to_home(mc, speed=60):
    mc.send_angles([90, 1, 0, 0, -90, 0], speed)
    mc.set_gripper_value(0, 50)

# Uses pynput to listen for key presses and control the robot's joints
def keyboard_control(mc, step=3):
    # Configuration
    speed = 30
    angles = mc.get_angles()
    gripper_open = True

    # Move a single joint
    def move_joint(joint_index, delta):
        current_angles = mc.get_angles()  # 🟢 Always get live values
        if current_angles is None:
            print("⚠️ Unable to read current angles.")
            return

        current_angles[joint_index] += delta
        mc.send_angles(current_angles, 60)
        print(f"Moved joint {joint_index+1} → {current_angles[joint_index]:.1f}°")
        print(f"Current coords: {mc.get_coords()}")

    # Toggle gripper open/close
    def toggle_gripper():
        nonlocal gripper_open
        gripper_open = not gripper_open
        mc.set_gripper_value(100 if gripper_open else 0, 70)
        print("Gripper opened." if gripper_open else "Gripper closed.")
        time.sleep(0.1)


    # Handle key presses
    def on_press(key):
        try:
            if key.char == 'q':
                move_joint(2, step)
            elif key.char == 'a':
                move_joint(2, -step)
            elif key.char == 'w':
                move_joint(3, step)
            elif key.char == 's':
                move_joint(3, -step)
            elif key.char == 'e':
                move_joint(4, step)
            elif key.char == 'd':
                move_joint(4, -step)
            elif key.char == 'r':
                move_joint(5, step)
            elif key.char == 'f':
                move_joint(5, -step)
            elif key.char == 'o':
                toggle_gripper()
            elif key.char == 'x':
                print("Returning to home position...")
                move_to_home(mc)
                return
        except AttributeError:
            if key == keyboard.Key.left:
                move_joint(0, -step)
            elif key == keyboard.Key.right:
                move_joint(0, step)
            elif key == keyboard.Key.up:
                move_joint(1, -step)
            elif key == keyboard.Key.down:
                move_joint(1, step)
            elif key == keyboard.Key.esc:
                print("Exiting...")
                return False

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press) as listener:
        print("Control started.")
        print("Arrow keys: Joints 1 & 2")
        print("Q/A, W/S, E/D, R/F: Joints 3–6")
        print("O: Toggle gripper | X: Home | ESC: Exit")
        listener.join()

def move_joint(mc, joint_index, delta):
    current_angles = mc.get_angles()  # 🟢 Always get live values
    if current_angles is None:
        print("⚠️ Unable to read angles.")
        return
    current_angles[joint_index] += delta
    mc.send_angles(current_angles, 60)
    print(f"✅ Moved joint {joint_index+1} → {current_angles[joint_index]:.1f}°")
    coords = mc.get_coords()
    if coords:
        print(f"📍 Current coords: {coords}")

gripper_open = [False] 
def toggle_gripper(mc):
    gripper_open[0] = not gripper_open[0]
    mc.set_gripper_value(15 if gripper_open[0] else 0, 70)
    print("✅ Gripper opened" if gripper_open[0] else "✅ Gripper closed")

def camera_keyboard_control(mc, move_joint, toggle_gripper, move_to_home, settings, show_camera_with_grid_frame):
    """
    Camera loop with keyboard control for the robot.
    Opens the camera window, shows grid overlay, and listens to key commands.
    """

    cap = cv2.VideoCapture(settings.CAMERA_INDEX)
    if not cap.isOpened():
        print("❌ Could not open camera.")
        return

    cv2.namedWindow("Robot Control", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Robot Control", settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)

    print("✅ Camera keyboard control started. Press ESC to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera read failed.")
            break

        # Resize and overlay grid
        frame = cv2.resize(frame, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        cv2.imshow("Robot Control", frame)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('z'):
            move_joint(mc, 0, settings.JOINT_STEP)
        elif key == ord('x'):
            move_joint(mc, 0, -settings.JOINT_STEP)
        elif key == ord('c'):
            move_joint(mc, 1, settings.JOINT_STEP)
        elif key == ord('v'):
            move_joint(mc, 1, -settings.JOINT_STEP)
        elif key == ord('q'):
            move_joint(mc, 2, settings.JOINT_STEP)
        elif key == ord('a'):
            move_joint(mc, 2, -settings.JOINT_STEP)
        elif key == ord('w'):
            move_joint(mc, 3, settings.JOINT_STEP)
        elif key == ord('s'):
            move_joint(mc, 3, -settings.JOINT_STEP)
        elif key == ord('e'):
            move_joint(mc, 4, settings.JOINT_STEP)
        elif key == ord('d'):
            move_joint(mc, 4, -settings.JOINT_STEP)
        elif key == ord('r'):
            move_joint(mc, 5, settings.JOINT_STEP)
        elif key == ord('f'):
            move_joint(mc, 5, -settings.JOINT_STEP)
        elif key == ord('o'):
            toggle_gripper(mc)
        elif key == ord('h'):
            print("🔄 Returning to home position...")
            move_to_home(mc)
            time.sleep(2)
            print("✅ Home position reached.")
        elif key == ord('p'):
            coords = mc.get_coords()
            if coords:
                print(f"📍 Current coords: {coords}")
                print("current angles:", mc.get_angles())
            else:
                print("⚠️ Unable to read coords.")
        elif key == 27:  # ESC
            print("✅ Exiting control mode.")
            break

    cap.release()
    cv2.destroyAllWindows()
