import os
import copy

from board_representation import Board, NonBlankSquareException, GameOverException, Mark
from minimax import minimax

SEARCH_DEPTH = int(os.getenv('SEARCH_DEPTH', '-1'))

def ai_play(board: Board):
    best_move = None
    best_move_score = None
    for i in board.available_squares:
        board_clone = copy.deepcopy(board)
        board_clone.place_mark(i)
        score = minimax(board_clone, SEARCH_DEPTH)
        if best_move_score is None:
            best_move = i
            best_move_score = score
        else:
            is_better = best_move_score < score if board.playing == Mark.NOUGHT else best_move_score > score
            if is_better:
                best_move = i
                best_move_score = score
    board.place_mark(best_move)


def main():
    board = Board()
    while board.is_still_on_play:
        try:
            print(board)
            square = int(input(f'Place your mark:')) - 1
            board.place_mark(square)
            ai_play(board)
        except NonBlankSquareException as ex:
            print(ex, "Try again")
        except ValueError:
            print("Enter a number ranging 1 to 9")
        except GameOverException:
            break
    if board.is_tic_tac_toe:
        print(board, f"\nTic-Tac-Toe! {board.playing.name} wins!")
    else:
        print(board, f"\nDraw!")


if __name__ == "__main__":
    main()
