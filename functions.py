import math
import time
# Puts the robot in home position
def move_to_home(mc, speed=60):
    mc.send_angles([0, 0, 0, 0, 0, 0], speed)
    mc.set_gripper_value(0, 50)
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
