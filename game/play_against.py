import chess
import chess.engine
from config.squares import square_angles
from robot.arm_control import pick_and_place_piece

STOCKFISH_PATH = r"C:\Users\leghlimia\Purdue Cobot\Purdue-Cobot\.venv\Lib\site-packages\stockfish\stockfish-windows-x86-64-avx2.exe"
def difficulty(tk, mc):
    def on_select_difficulty(level):
        depth_levels = {
            "Easy": 1,
            "Medium": 5,
            "Hard": 12
        }
        depth = depth_levels[level]
        window.destroy()
        play_against_robot_chess(mc, depth=depth)

    window = tk.Tk()
    window.title("Choose Chess Difficulty")
    window.geometry("300x200")

    tk.Label(window, text="Select Difficulty:", font=("Arial", 14)).pack(pady=10)

    for level in ["Easy", "Medium", "Hard"]:
        tk.Button(window, text=level, width=20, command=lambda l=level: on_select_difficulty(l)).pack(pady=5)

    window.mainloop()

# Flip a square name as if rotating the board 180 degrees
# E.g., a1 -> h8, b2 -> g7, etc.
def rename_squares_for_black(square_angles):
    """
    Re-map square names assuming the robot is physically using a1-h2,
    but logically playing as Black (so a1 becomes h8, a2 becomes h7, etc.).
    """
    renamed = {}
    for square, angles in square_angles.items():
        file = square[0]
        rank = square[1]

        # Flip both file and rank
        flipped_file = chr(ord('h') - (ord(file) - ord('a')))
        flipped_rank = str(9 - int(rank))

        new_name = flipped_file + flipped_rank
        renamed[new_name] = angles

    return renamed

def play_against_robot_chess(mc, robot_color='black', depth=4):
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)


    if robot_color.lower() == "black":
        angle_map = rename_squares_for_black(square_angles)
    else:
        angle_map = square_angles

    while not board.is_game_over():
        print("\nCurrent board:\n", board)

        # Human plays
        try:
            move = input("Your move (e.g. e2e4): ")
            if move.lower() == 'exit':
                print("Exiting game.")
                break
            board.push_uci(move)
        except:
            print("Invalid move. Try again.")
            continue

        if board.is_game_over():
            break

        # Stockfish responds
        result = engine.play(board, chess.engine.Limit(depth=depth))
        move = result.move
        from_square = chess.square_name(move.from_square)
        to_square = chess.square_name(move.to_square)
        print("Stockfish plays:", move)

        promotion = move.promotion  # This will be a chess.PieceType or None
        if promotion:
            print(f"Stockfish promotes pawn to: {chess.piece_name(promotion)}")
            # Optional: Add logic to swap physical pawn with a queen

        # Get angles from your config
        from_angles = angle_map[from_square]
        to_angles = angle_map[to_square]

        # Move the piece with the robot
        pick_and_place_piece(mc, from_square, from_angles, to_square, to_angles)

        # Update the board
        board.push(move)

    print("\nGame over. Result:", board.result())
    engine.quit()
    return board.result()