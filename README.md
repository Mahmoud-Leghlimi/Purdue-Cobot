# 🤖 Robotic Chess Player using MyCobot 320

**Author:** Mahmoud Leghlimi  
**Email:** mahmoudboston99@gmail.com , leghlimia@berea.edu  
**LinkedIn:** [LinkedIn Mahmoud](https://www.linkedin.com/in/mahmoud-leghlimi-58aa19176/)  
**Internship:** Bechtel Center, Purdue School of Engineering (Summer 2025)  

---

## 📝 Description

This project integrates computer vision, motion planning, and robot control to create a robotic arm that can play physical chess using the [MyCobot 320](https://www.elephantrobotics.com/mycobot320/). The user can either manually operate the robot using a keyboard interface or play against an AI opponent powered by Stockfish.

The project is intended to explore affordable and accessible robotics platforms for vision-guided automation, particularly in resource-constrained environments.

---

## 🎮 Features

- Interactive UI with Tkinter for selecting between control modes
- Two modes:  
  - **Play With Robot**: Use your hand to move pieces, then click source/destination to let the robot mirror the move  
  - **Play Against Robot**: Play chess against Stockfish; the robot physically plays its moves
- Custom camera overlay with grid-based square detection using OpenCV
- Hand-calibrated joint angles mapped to chessboard coordinates
- Manual keyboard control for direct joint and gripper movement
- Safety-handling for gripper behavior and rotation limits

---

## 🧠 Technologies Used

- Python
- OpenCV (vision/grid overlay)
- `pymycobot` (robot control)
- `python-chess` (game engine)
- Stockfish (AI opponent)
- Tkinter (GUI)

---

## 📂 Folder Structure

```
Purdue-Cobot/
│
├── app.py                      # Main GUI launcher
├── robot/
│   ├── play_with_robot.py      # Click-to-move interaction
│   ├── arm_control.py          # Low-level arm control helpers
│   └── camera_keyboard_control.py # Manual control with key presses
│
├── config/
│   ├── squares.py              # Pre-recorded joint angles per square
│   └── settings.py             # Window and board config
│
functions.py            # General-purpose utilities
│
└── README.md
```

---

## 🧪 How Calibration Works

- Each square (e.g. `'a2'`) is associated with joint angles in `config/squares.py`
- Initial angles were obtained by manually moving the arm and reading its position
- Refinement was done using keyboard-based fine-tuning
- Lower squares near the base (`a1`, `b2`, etc.) required longer delay due to higher torque and reorientation instability
- Calibration references:
  - Rojas Úrzulo et al. (2023)
  - Realman SDK Docs (2025)
  - Song et al. (2025)

---

## 🚀 Getting Started

1. Clone the repository  
2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```
3. Connect the MyCobot 320 over USB (default: `COM8`)  
4. Run the GUI  
   ```bash
   python app.py
   ```
5. Choose the the desired mode

---

## 🧑‍💻 Keyboard Controls

| Key | Action             |
|-----|--------------------|
| z/x | Joint 1 +/-        |
| c/v | Joint 2 +/-        |
| q/a | Joint 3 +/-        |
| w/s | Joint 4 +/-        |
| e/d | Joint 5 +/-        |
| r/f | Joint 6 +/-        |
| o   | Toggle gripper     |
| h   | Return to home     |
| p   | Print coords       |
| ESC | Exit control       |

---

## Play with Robot
"Playing with robot" functionality does not have chess logic implemented. It is completely the player's responsibility to insure game logic and rules are followed.
## Play Against Robot Documentation
In the "Play Against Robot" mode, the user plays their own move and inputs it using the syntax e2e4 (indicating the piece movement from e2 to e4), after which the robot physically makes the move. Then, the robot plays its own move, and the cycle continues, alternating between the user and the robot.

### How it Works:
**1. User's Move:** The user manually plays their move on the chessboard. The move must be entered in standard algebraic notation, such as e2e4, where the first two characters represent the source square, and the last two characters represent the destination square.

**2. Input Syntax:** The user inputs their move using the format source_square + destination_square, e.g., e2e4 for moving a piece from e2 to e4.

**3. Robot Executes User's Move:** Once the move is inputted, the robot will physically move the piece on the chessboard according to the user's specified move.

**4. AI Move (Stockfish):** After executing the user's move, Stockfish, the AI engine, generates the next move for the robot. The robot will then execute its move on the chessboard in the same manner.

**5. Game Continues:** The cycle alternates between the user and the robot, with each player making one move at a time. The robot's moves are executed physically on the board, and the game progresses until it ends.

## Edit coords
This functionality was added to give users more flexibility and choice in their experience. In case the standard chess board was changed or some angles needed adjustments then the user can use this functionality for their benefit.
### How to use
1. Either use the keyboard control or a self-written program to move the robot.
2. Use the keyboard function to print both the angles and coords (by clicking the P key). 
3. Copy the angles list and paste into the desired square in the library using the edit_coords functionality.
4. Click on the "save" button to save changes.

## 🧠 Acknowledgments

This work was completed as part of a hands-on robotics research internship with guidance and resources provided by the Bechtel Innovation Design Center at Purdue University under supervision of Dr Paul McPherson.
