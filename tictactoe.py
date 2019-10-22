import sys
import copy

from enum import Enum


class Status(Enum):
    PLAYING = 0
    DRAW = 1
    CROSS_WON = 2
    NOUGHT_WON = 3


class Mark(Enum):
    CROSS = 'x'
    NOUGHT = 'o'
    BLANK = ' '


class NonBlankSquareException(Exception):
    def __init__(self, square):
        super().__init__(f'Square {square} is not blank')


class Board:
    rays = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6))

    __maximizer = Mark.NOUGHT

    def __init__(self, grid=None, playing=Mark.NOUGHT, status=Status.PLAYING):
        self.grid = grid or [Mark.BLANK] * 9
        self.playing = playing
        self.status = status
        self.__is_tic_tac_toe = False

    def __str__(self):
        rows = []
        for ray in ((6, 7, 8), (3, 4, 5), (0, 1, 2)):
            rows.append('|'.join(self.grid[r].value for r in ray))
        grid = '\n-----\n'.join(rows)
        grid += f'\nPlaying: {self.playing.name}'
        grid += f'\nStatus: {self.status.name}'
        grid += f'\nScore: {self.get_board_score()}'
        return grid

    def place_mark(self, square):
        if self.grid[square] != Mark.BLANK:
            raise NonBlankSquareException(square)
        self.grid[square] = self.playing

    def is_a_draw(self):
        it_is = not any(m == Mark.BLANK
                        for m in self.grid) and self.status == Status.PLAYING
        return it_is

    def is_tic_tac_toe(self):
        if not self.__is_tic_tac_toe:
            for ray in self.rays:
                is_tic_tac_toe = all(self.grid[r] == self.playing for r in ray)
                if is_tic_tac_toe:
                    self.__is_tic_tac_toe = True
                    break
        return self.__is_tic_tac_toe

    def shift_turns(self):
        if self.is_still_on_play():
            self.playing = Mark.CROSS if self.playing == Mark.NOUGHT else Mark.NOUGHT

    def update_status(self):
        if self.is_tic_tac_toe():
            self.status = Status.CROSS_WON if self.playing == Mark.CROSS else Status.NOUGHT_WON
        elif self.is_a_draw():
            self.status = Status.DRAW
        else:
            self.status = Status.PLAYING

    def is_still_on_play(self):
        return self.status == Status.PLAYING

    def get_board_score(self):
        """
        Evaluation function
        """
        score = 0
        if self.is_tic_tac_toe():
            score += 10 if self.playing == self.__maximizer else -10
        return score

    def is_maximizer_playing(self):
        return self.__maximizer == self.playing


def play(board: Board, square: int):
    board.place_mark(square)
    board.update_status()
    board.shift_turns()


def minimax(board: Board, depth: int, is_maximizer: bool):
    score = 0
    if board.is_tic_tac_toe() or board.is_a_draw() or depth == 0:
        score = board.get_board_score()
    elif is_maximizer:
        best_score = -10**100
        for i in range(9):
            try:
                board_clone = copy.deepcopy(board)
                play(board_clone, i)
                score = minimax(board_clone, depth - 1, False)
                best_score = max(best_score, score)
            except NonBlankSquareException:
                pass
        score = best_score
    else:
        best_score = 10**100
        for i in range(9):
            try:
                board_clone = copy.deepcopy(board)
                play(board_clone, i)
                score = -minimax(board_clone, depth - 1, True)
                best_score = min(best_score, score)
            except NonBlankSquareException:
                pass
        score = best_score

    return score - depth


def ai_play(board: Board):
    best_move = None
    for i in range(9):
        try:
            board_clone = copy.deepcopy(board)
            play(board_clone, i)
            score = minimax(board_clone, 3, board_clone.is_maximizer_playing())
            if best_move is None or best_move < abs(score):
                best_move = i
        except NonBlankSquareException:
            pass
    play(board, best_move)


if __name__ == "__main__":
    board = Board()
    while board.is_still_on_play():
        try:
            print(board)
            square = int(input(f'Place your mark:')) - 1
            play(board, square)
            if board.is_still_on_play():
                ai_play(board)
        except NonBlankSquareException as ex:
            print(ex, "Try again")
        except ValueError:
            print("Enter a number ranging 1 to 9")
    print(board, f"\nTic-Tac-Toe! {board.playing.name} wins!")
