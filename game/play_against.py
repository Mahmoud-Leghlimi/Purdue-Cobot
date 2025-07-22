import chess
import chess.engine
from config.squares import square_angles
from robot.arm_control import pick_and_place_piece

STOCKFISH_PATH = r"C:\Users\leghlimia\Purdue Cobot\Purdue-Cobot\.venv\Lib\site-packages\stockfish\stockfish-windows-x86-64-avx2.exe"

def play_against_robot_chess(mc):
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

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
        result = engine.play(board, chess.engine.Limit(time=0.1))
        move = result.move
        from_square = chess.square_name(move.from_square)
        to_square = chess.square_name(move.to_square)
        print("Stockfish plays:", move)

        # Get angles from your config
        from_angles = square_angles[from_square]
        to_angles = square_angles[to_square]

        # Move the piece with the robot
        pick_and_place_piece(mc, from_square, from_angles, to_square, to_angles)

        # Update the board
        board.push(move)

    print("\nGame over. Result:", board.result())
    engine.quit()