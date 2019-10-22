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

    def __init__(self, grid=None, playing=Mark.NOUGHT, status=Status.PLAYING):
        self.grid = grid or [Mark.BLANK] * 9
        self.playing = playing
        self.status = status

    def __str__(self):
        rows = []
        for ray in ((6, 7, 8), (3, 4, 5), (0, 1, 2)):
            rows.append('|'.join(self.grid[r].value for r in ray))
        grid = '\n-----\n'.join(rows)
        grid += f'\nPlaying: {self.playing.name}'
        grid += f'\nStatus: {self.status.name}'
        return grid

    def place_mark(self, square):
        if self.grid[square] != Mark.BLANK:
            raise NonBlankSquareException(square)
        self.grid[square] = self.playing

    def is_a_draw(self):
        it_is = not any(m == Mark.BLANK for m in self.grid)
        return it_is

    def is_tic_tac_toe(self):
        it_is = False
        for ray in self.rays:
            is_tic_tac_toe = all(self.grid[r] == self.playing for r in ray)
            if is_tic_tac_toe:
                it_is = True
                break
        return it_is

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


if __name__ == "__main__":
    board = Board()
    while board.is_still_on_play():
        try:
            print(board)
            square = int(input(f'Place your mark:')) - 1
            board.place_mark(square)
            board.update_status()
            board.shift_turns()
        except NonBlankSquareException as ex:
            print(ex, "Try again")
        except ValueError:
            print("Enter a number ranging 1 to 9")
    print(board, f"\nTic-Tac-Toe! {board.playing.name} wins!")
