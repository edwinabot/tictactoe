from enum import Enum


class Status(Enum):
    PLAYING = 0
    DRAW = 1
    CROSS_WON = 2
    NOUGHT_WON = 3


class Square(Enum):
    CROSS = 'x'
    NOUGHT = 'o'
    EMPTY = ' '


class Board:
    def __init__(self,
                 grid=None,
                 playing=Square.NOUGHT,
                 status=Status.PLAYING):
        self.grid = grid or [Square.EMPTY] * 9
        self.playing = playing
        self.status = status

    def __str__(self):
        grid = '\n-----\n'.join(['|'.join(s.value for s in self.grid[i:i+3]) for i in range(3)])
        grid += f'\nPlaying: {self.playing}'
        grid += f'\nStatus: {self.status}'
        return grid


if __name__ == "__main__":
    board = Board()
    print(board)
