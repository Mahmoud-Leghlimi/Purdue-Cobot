import cv2

# Open the default camera (usually webcam)
cap = cv2.VideoCapture(1)  # Use 1 or 2 if you have multiple cameras

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

print("🎥 Camera opened successfully. Press 's' to save frame, 'q' to quit.")

ROWS = 8
COLS = 8

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get frame dimensions
    height, width, _ = frame.shape
    cell_height = height // ROWS
    cell_width = width // COLS

    # Draw horizontal lines
    for i in range(1, ROWS):
        y = i * cell_height
        cv2.line(frame, (0, y), (width, y), (0, 255, 0), 1)

    # Draw vertical lines
    for j in range(1, COLS):
        x = j * cell_width
        cv2.line(frame, (x, 0), (x, height), (0, 255, 0), 1)

    # Optional: Label the squares
    for row in range(ROWS):
        for col in range(COLS):
            x = col * cell_width + 5
            y = row * cell_height + 20
            square_name = chr(ord('a') + col) + str(8 - row)
            cv2.putText(frame, square_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

    # Show the result
    cv2.imshow("Chessboard Grid", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release camera and close window
cap.release()
cv2.destroyAllWindows()