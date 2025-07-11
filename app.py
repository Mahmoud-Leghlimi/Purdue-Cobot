import tkinter as ttk
from tkinter import messagebox
import threading

from config import settings, squares
from robot import arm_control
from robot.arm_control import camera_keyboard_control
from vision.camera_grid import show_camera_with_grid_frame

# 🔌 Global robot connection
mc = None
def open_edit_coords_window():
    edit_win = ttk.Toplevel()
    edit_win.title("Edit Square Coordinates")
    edit_win.geometry("400x400")

    # Dropdown to select square
    selected_square = ttk.StringVar(value=list(squares.square_coords.keys())[0])
    square_menu = ttk.Combobox(
        edit_win,
        textvariable=selected_square,
        values=list(squares.square_coords.keys()),
        state="readonly"
    )
    square_menu.pack(pady=10)

    # Entries for coords
    entries = []
    labels = ["X", "Y", "Z", "Rx", "Ry", "Rz"]
    for label in labels:
        frame = ttk.Frame(edit_win)
        frame.pack(pady=2)
        ttk.Label(frame, text=label).pack(side="left")
        entry = ttk.Entry(frame)
        entry.pack(side="right")
        entries.append(entry)

    # Load current coords when square changes
    def load_coords(*args):
        coords = squares.square_coords.get(selected_square.get(), [0,0,0,0,0,0])
        for i, val in enumerate(coords):
            entries[i].delete(0, ttk.END)
            entries[i].insert(0, str(val))

    selected_square.trace_add("write", load_coords)
    load_coords()

    # Save button
    def save_coords():
        try:
            new_values = [float(e.get()) for e in entries]
            squares.square_coords[selected_square.get()] = new_values
            messagebox.showinfo("Success", f"Updated {selected_square.get()} coordinates.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    ttk.Button(edit_win, text="Save Changes", command=save_coords).pack(pady=10)
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
    print("🔌 Connecting to MyCobot...")
    mc = arm_control.connect_robot()

    if mc:
        print("✅ Successfully connected to MyCobot!")
    else:
        print("❌ Failed to connect to MyCobot!")
        messagebox.showerror(
            "Connection Error",
            "❌ Could not connect to MyCobot. Check your COM port!"
        )
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

    ttk.Button(
    root,
    text="Edit Square Coordinates",
    font=("Helvetica", 12),
    width=20,
    command=open_edit_coords_window
    ).pack(pady=10)

    root.mainloop()

# ---------- PROGRAM START ----------
if __name__ == "__main__":
    main_window()