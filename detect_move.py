import cv2
import time
from pymycobot import MyCobot320
from config.squares import square_angles

# --- Robot Setup ---
mc = MyCobot320("COM8", 115200)

def move_robot_to(angles):
    print(f"🤖 Moving to {angles}")
    mc.send_angles(angles, 60, 0)
    time.sleep(2)

# --- Define chessboard region in camera view (adjust to your camera!) ---
ROI_TOP = 100
ROI_BOTTOM = 500
ROI_LEFT = 100
ROI_RIGHT = 500
ROI_WIDTH = ROI_RIGHT - ROI_LEFT
ROI_HEIGHT = ROI_BOTTOM - ROI_TOP

# --- Open Camera ---
cap = cv2.VideoCapture(0)
cv2.namedWindow("Chess Grid")

# --- Mouse Click Handler ---
def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if ROI_LEFT <= x <= ROI_RIGHT and ROI_TOP <= y <= ROI_BOTTOM:
            col = (x - ROI_LEFT) * 8 // ROI_WIDTH
            row = (y - ROI_TOP) * 8 // ROI_HEIGHT
            square = chr(ord('a') + col) + str(8 - row)
            print(f"🖱️ Clicked on: {square}")

            if square in square_angles:
                move_robot_to(square_angles[square])
            else:
                print("❌ Square not in map.")

cv2.setMouseCallback("Chess Grid", on_mouse)

# --- Main Loop ---
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera read failed.")
        break

    # Draw the chessboard ROI on the frame
    roi = frame[ROI_TOP:ROI_BOTTOM, ROI_LEFT:ROI_RIGHT]

    # Draw 8x8 grid on ROI
    square_w = ROI_WIDTH // 8
    square_h = ROI_HEIGHT // 8

    for i in range(1, 8):
        cv2.line(roi, (0, i * square_h), (ROI_WIDTH, i * square_h), (0,255,0), 1)
        cv2.line(roi, (i * square_w, 0), (i * square_w, ROI_HEIGHT), (0,255,0), 1)

    # Draw ROI back on original frame
    frame[ROI_TOP:ROI_BOTTOM, ROI_LEFT:ROI_RIGHT] = roi

    cv2.imshow("Chess Grid", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
