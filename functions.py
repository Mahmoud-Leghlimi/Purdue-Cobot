# Puts the robot in home position
def move_to_home(mc, speed=80):
    mc.send_angles([0, 0, 0, 0, 0, 0], speed)