import math
import time
from pynput import keyboard
# Puts the robot in home position
def move_to_home(mc, speed=60):
    mc.send_angles([0, 0, 0, 0, 0, 0], speed)
    mc.set_gripper_value(0, 50)


# Function to run transfer cycles between two points
# point_a and point_b are lists of angles for the robot's joints
def run_transfer_cycles(mc, point_a, point_b):

    # Move function
    def move_to(angles, speed=60, pause=3):
        mc.send_angles(angles, speed)
        time.sleep(pause)

    # Gripper control
    def grip(open_grip: bool, strength=50, pause=1):
        if open_grip:
            mc.set_gripper_value(100, strength)  # Open
        else:
            mc.set_gripper_value(0, strength)    # Close
        time.sleep(pause)

    # One full transfer cycle: A → B, back; B → A, back
    def transfer_cycle():
        move_to_home(mc)

        # A → B
        grip(open_grip=True)
        move_to(point_a)
        time.sleep(1)
        grip(open_grip=False)
        move_to(point_b)
        grip(open_grip=True)

        move_to_home(mc)

        # B → A
        grip(open_grip=True)
        move_to(point_b)
        grip(open_grip=False)
        move_to(point_a)
        grip(open_grip=True)

        move_to_home(mc)
    transfer_cycle()

# Function to control the robot using keyboard input
# Uses pynput to listen for key presses and control the robot's joints
def keyboard_control(mc):
    # Configuration
    step = 2
    speed = 30
    angles = mc.get_angles()
    gripper_open = True

    # Move a single joint
    def move_joint(joint_index, delta):
        angles[joint_index] += delta
        mc.send_angle(joint_index + 1, angles[joint_index], speed)
        print(f"Joint {joint_index+1} → {angles[joint_index]:.1f}°")
        time.sleep(0.1)

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