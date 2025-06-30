# main.py
from robot.arm_control import connect_robot, keyboard_control
from config import settings
import cv2
from vision.camera_grid import show_camera_with_grid_frame

def main():
    print("🎥 Starting camera...")
    cap = cv2.VideoCapture(settings.CAMERA_INDEX)
    if not cap.isOpened():
        print("❌ Failed to open camera.")
        return

    cv2.namedWindow("Chess Grid", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Chess Grid", settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera read failed.")
            break

        frame = cv2.resize(frame, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        frame = show_camera_with_grid_frame(frame)
        cv2.imshow("Chess Grid", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            print("✅ Exiting...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()