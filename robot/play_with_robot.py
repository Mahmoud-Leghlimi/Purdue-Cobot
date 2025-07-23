import cv2
import time
from pymycobot import MyCobot320
from config.squares import square_angles
from functions import move_to_home
from config import settings

def play_with_robot_click(mc, tk):
    """
    Opens the camera with an 8x8 grid ROI.
    Lets the user click a source and a destination square,
    shows the selected squares live on the feed,
    and asks for confirmation before moving the robot
    to execute pick-and-place between them.
    """

    # --- ROI Settings ---
    square_size = settings.SQUARE_SIZE
    grid_w = square_size * settings.GRID_COLS
    grid_h = square_size * settings.GRID_ROWS
    win_w = settings.WINDOW_WIDTH
    win_h = settings.WINDOW_HEIGHT

    ROI_LEFT = (win_w - grid_w) // 2
    ROI_TOP = (win_h - grid_h) // 2
    ROI_RIGHT = ROI_LEFT + grid_w
    ROI_BOTTOM = ROI_TOP + grid_h
    ROI_WIDTH = grid_w
    ROI_HEIGHT = grid_h

    clicks = []

    # --- Robot Movement Helpers ---
    def move_robot_to(square, angles):
        print(f"🤖 Moving to joint angles: {angles}")
        mc.send_angles(angles, 40)

        # Conditional wait time
        if '1' in square or '2' in square:
            time.sleep(4)
        else:
            time.sleep(7)

    def pick_and_place_piece(source_square, source_angles, dest_square, dest_angles):
        print("🔄 Returning to home before pick...")
        move_to_home(mc)
        time.sleep(1)

        mc.set_gripper_value(15, 50)  # open gripper
        time.sleep(4)

        print(f"🤖 Moving to pick: {source_angles}")
        move_robot_to(source_square, source_angles)

        mc.set_gripper_value(0, 50)  # close gripper
        time.sleep(4)

        move_to_home(mc)
        print("✅ Piece picked and returned home.")

        print("🔄 Returning to home before place...")
        time.sleep(1)

        print(f"🤖 Moving to place: {dest_angles}")
        move_robot_to(dest_square, dest_angles)

        mc.set_gripper_value(15, 50)  # open gripper to release
        time.sleep(3)

        move_to_home(mc)
        print("✅ Piece placed and returned home.")

    def confirm_move(source, dest):
        root = tk.Tk()
        root.withdraw()
        result = tk.messagebox.askyesno(
            "Confirm Move",
            f"Move from {source} to {dest}?\n\nClick 'Yes' to proceed."
        )
        root.destroy()
        return result

    # --- Camera Setup ---
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Play with the Robot")

    selected_squares = [None, None]  # store for overlay

    # --- Mouse Click Handler ---
    def on_mouse(event, x, y, flags, param):
        nonlocal selected_squares

        if event == cv2.EVENT_LBUTTONDOWN:
            if ROI_LEFT <= x <= ROI_RIGHT and ROI_TOP <= y <= ROI_BOTTOM:
                col = (x - ROI_LEFT) * 8 // ROI_WIDTH
                row = (y - ROI_TOP) * 8 // ROI_HEIGHT
                square = chr(ord('a') + col) + str(8 - row)
                print(f"🖱️ Clicked on: {square}")

                if square in square_angles:
                    clicks.append(square)
                    if len(clicks) > 2:
                        clicks.pop(0)

                    # Update overlay labels
                    if len(clicks) == 1:
                        selected_squares = [clicks[0], None]
                    elif len(clicks) == 2:
                        selected_squares = [clicks[0], clicks[1]]

                        # --- Ask for confirmation ---
                        print(f"\n🟢 Selected Move: {clicks[0]} ➜ {clicks[1]}")
                        if confirm_move(clicks[0], clicks[1]):
                            print("✅ Move confirmed!")
                            pick_and_place_piece(
                                clicks[0],
                                square_angles[clicks[0]],
                                clicks[1],
                                square_angles[clicks[1]]
                            )
                        else:
                            print("❌ Move canceled.")

                        # Reset
                        clicks.clear()
                        selected_squares = [None, None]

                else:
                    print("❌ Square not in angle map.")

    cv2.setMouseCallback("Play with the Robot", on_mouse)

    # --- Main Loop ---
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (win_w, win_h))
        if not ret:
            print("❌ Camera read failed.")
            break

        # Draw ROI
        roi = frame[ROI_TOP:ROI_BOTTOM, ROI_LEFT:ROI_RIGHT]
        square_w = ROI_WIDTH // 8
        square_h = ROI_HEIGHT // 8

        # Draw grid lines
        for i in range(1, 8):
            cv2.line(roi, (0, i * square_h), (ROI_WIDTH, i * square_h), (0, 255, 0), 1)
            cv2.line(roi, (i * square_w, 0), (i * square_w, ROI_HEIGHT), (0, 255, 0), 1)

        # Overlay selected squares
        for idx, sq in enumerate(selected_squares):
            if sq:
                col = ord(sq[0]) - ord('a')
                row = 8 - int(sq[1])
                x1 = col * square_w
                y1 = row * square_h
                x2 = x1 + square_w
                y2 = y1 + square_h

                color = (0, 255, 255) if idx == 0 else (0, 0, 255)
                cv2.rectangle(roi, (x1, y1), (x2, y2), color, 2)
                label = "SRC" if idx == 0 else "DST"
                cv2.putText(roi, f"{label}: {sq}", (x1 + 5, y1 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Draw back ROI
        frame[ROI_TOP:ROI_BOTTOM, ROI_LEFT:ROI_RIGHT] = roi

        cv2.imshow("Play with the Robot", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()