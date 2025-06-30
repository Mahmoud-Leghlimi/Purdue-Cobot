import tkinter as ttk
from tkinter import messagebox
import threading

from config import settings
from robot import arm_control
from robot.arm_control import camera_keyboard_control
from vision.camera_grid import show_camera_with_grid_frame

# 🔌 Global robot connection
mc = None

# ---------- LOG FUNCTION ----------
def play_with_robot():
    messagebox.showinfo(
        "Coming Soon",
        "🤖 'Play with the Robot' functionality will be added here!"
    )

def play_against_robot():
    messagebox.showinfo(
        "Coming Soon",
        "🤖 'Play Against the Robot' functionality will be added here!"
    )
def log(message):
    if log_display:
        log_display.insert(ttk.END, message + "\n")
        log_display.see(ttk.END)

# ---------- CAMERA CONTROL LAUNCH ----------
def launch_camera_control():
    """
    Start the camera control in a separate thread so the GUI doesn't freeze.
    """
    threading.Thread(target=lambda: camera_keyboard_control(
        mc,
        arm_control.move_joint,
        arm_control.toggle_gripper,
        arm_control.move_to_home,
        settings,
        show_camera_with_grid_frame
    ), daemon=True).start()

# ---------- SECOND WINDOW ----------
def keyboard_control_window():
    control_win = ttk.Tk()
    control_win.title("Keyboard Control")
    control_win.geometry("800x500")
    control_win.resizable(True, True)

    ttk.Label(
        control_win,
        text="Keyboard Control Instructions",
        font=("Helvetica", 16, "bold")
    ).pack(pady=10)

    instructions = (
        "Keyboard Controls:\n\n"
        "z / x : Joint 1\n"
        "c / v : Joint 2\n"
        "q / a : Joint 3\n"
        "w / s : Joint 4\n"
        "e / d : Joint 5\n"
        "r / f : Joint 6\n"
        "o     : Toggle gripper\n"
        "h     : Return home\n"
        "p     : Print coordinates\n"
        "ESC   : Exit control\n"
    )
    ttk.Label(
        control_win,
        text=instructions,
        font=("Courier", 10),
        justify="left",
        anchor="w",
        bg="#f0f0f0",
        relief="groove",
        bd=2
    ).pack(padx=10, pady=10, fill="x")

    ttk.Button(
        control_win,
        text="Start Camera + Control",
        font=("Helvetica", 12),
        command=launch_camera_control
    ).pack(pady=15)

    global log_display
    log_display = ttk.Text(control_win, height=10, width=60)
    log_display.pack(padx=10, pady=10)
    log_display.insert(ttk.END, "✅ Ready.\n")

    control_win.mainloop()

# ---------- MAIN WINDOW ----------
def main_window():
    root = ttk.Tk()
    root.title("Robotic Arm Controller")
    root.geometry("500x500")
    root.resizable(False, False)

    ttk.Label(
        root,
        text="Robotic Arm Controller",
        font=("Helvetica", 16, "bold")
    ).pack(pady=20)

    ttk.Button(
        root,
        text="Keyboard Control",
        font=("Helvetica", 12),
        width=20,
        command=lambda: [root.destroy(), keyboard_control_window()]
    ).pack(pady=10)

    ttk.Button(
        root,
        text="Play with the Robot",
        font=("Helvetica", 12),
        width=20,
        command=play_with_robot
    ).pack(pady=10)

    ttk.Button(
        root,
        text="Play Against the Robot",
        font=("Helvetica", 12),
        width=20,
        command=play_against_robot
    ).pack(pady=10)

    root.mainloop()

# ---------- PROGRAM START ----------
if __name__ == "__main__":
    print("🔌 Connecting to MyCobot...")
    mc = arm_control.connect_robot()

    if mc:
        print("✅ Successfully connected to MyCobot!")
        main_window()
    else:
        print("❌ Failed to connect to MyCobot!")
        messagebox.showerror(
            "Connection Error",
            "❌ Could not connect to MyCobot. Check your COM port!"
        )