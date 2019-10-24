import sys
import copy

from board_representation import Board, NonBlankSquareException, Mark


def evaluate(board: Board):
    score = 0
    if board.is_tic_tac_toe:
        score = score + 10 if board.playing == Mark.NOUGHT else score - 10
    elif board.is_a_draw:
        score = 0
    return score


def minimize(board: Board, depth: int):
    if not board.is_still_on_play or depth == 0:
        return evaluate(board)

    best_score = 10**100
    for i in board.available_squares:
        try:
            board_clone = copy.deepcopy(board)
            board_clone.place_mark(i)
            score = maximize(board_clone, depth - 1)
            best_score = min(best_score, score)
        except NonBlankSquareException:
            pass
    return best_score


def maximize(board: Board, depth: int):
    if not board.is_still_on_play or depth == 0:
        return evaluate(board)

    best_score = -10**100
    for i in board.available_squares:
        board_clone = copy.deepcopy(board)
        board_clone.place_mark(i)
        score = minimize(board_clone, depth - 1)
        best_score = max(best_score, score)
    return best_score


def minimax(board: Board, depth: int):
    if board.playing == Mark.NOUGHT:
        return maximize(board, depth)
    else:
        return minimize(board, depth)
