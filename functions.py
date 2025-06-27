import math
import time
from pynput import keyboard
# Puts the robot in home position
def move_to_home(mc, speed=60):
    mc.send_angles([90, 1, 0, 0, -90, 0], speed)
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

# Function to go to a square grab a piece and put it on another square
def move_piece(mc, source, dest, square_coords):
    # Move above source
    above_source = square_coords[source][:]
    above_source[2] += 40  # raise z
    mc.send_coords(above_source, 60, 0)
    time.sleep(1)

    # Open gripper first
    mc.set_gripper_value(100, 70)
    time.sleep(1)

    # Lower to pick
    mc.send_coords(square_coords[source], 60, 0)
    time.sleep(1)

    # Close gripper
    mc.set_gripper_value(0, 70)
    time.sleep(1)

    # Raise piece
    mc.send_coords(above_source, 60, 0)
    time.sleep(1)

    # Move above destination
    above_dest = square_coords[dest][:]
    above_dest[2] += 30
    mc.send_coords(above_dest, 60, 0)
    time.sleep(1)

    # Lower to place
    mc.send_coords(square_coords[dest], 60, 0)
    time.sleep(1)

    # Open gripper
    mc.set_gripper_value(100, 70)
    time.sleep(1)

    # Raise arm again
    mc.send_coords(above_dest, 60, 0)