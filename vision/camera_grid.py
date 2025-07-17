import cv2
from config import settings

import cv2
from config import settings

def show_camera_with_grid_frame(frame):
    # Resize frame to match window size
    frame = cv2.resize(frame, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

    # Grid size
    square_w = settings.SQUARE_SIZE
    square_h = settings.SQUARE_SIZE
    grid_width = square_w * settings.GRID_COLS
    grid_height = square_h * settings.GRID_ROWS

    # Calculate top-left corner of the grid (centered)
    start_x = (settings.WINDOW_WIDTH - grid_width) // 2
    start_y = (settings.WINDOW_HEIGHT - grid_height) // 2

    # Draw horizontal grid lines
    for i in range(settings.GRID_ROWS + 1):
        y = start_y + i * square_h
        cv2.line(frame, (start_x, y), (start_x + grid_width, y), (0, 255, 0), 1)

    # Draw vertical grid lines
    for j in range(settings.GRID_COLS + 1):
        x = start_x + j * square_w
        cv2.line(frame, (x, start_y), (x, start_y + grid_height), (0, 255, 0), 1)

    # Draw chess square labels
    for row in range(settings.GRID_ROWS):
        for col in range(settings.GRID_COLS):
            label = chr(ord('a') + col) + str(8 - row)
            text_x = start_x + col * square_w + 5
            text_y = start_y + row * square_h + 20
            cv2.putText(frame, label, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

    return frame