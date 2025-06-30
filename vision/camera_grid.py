import cv2
from config import settings

import cv2
from config import settings

def show_camera_with_grid_frame(frame):
    """
    Takes a camera frame, overlays an 8x8 grid with labels (a1–h8),
    and returns the modified frame.
    """

    frame_h, frame_w = frame.shape[:2]
    square_h = frame_h // settings.GRID_ROWS
    square_w = frame_w // settings.GRID_COLS

    # Draw horizontal grid lines
    for i in range(1, settings.GRID_ROWS):
        y = i * square_h
        cv2.line(frame, (0, y), (frame_w, y), (0, 255, 0), 1)

    # Draw vertical grid lines
    for j in range(1, settings.GRID_COLS):
        x = j * square_w
        cv2.line(frame, (x, 0), (x, frame_h), (0, 255, 0), 1)

    # Add chess square labels (a1–h8)
    for row in range(settings.GRID_ROWS):
        for col in range(settings.GRID_COLS):
            label = chr(ord('a') + col) + str(8 - row)
            text_x = col * square_w + 5
            text_y = row * square_h + 20
            cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

    return frame