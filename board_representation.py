from enum import Enum


class NonBlankSquareException(Exception):
    def __init__(self, square):
        super().__init__(f'Square {square} is not blank')


class GameOverException(Exception):
    def __init__(self):
        super().__init__(f'Game over')


class Status(Enum):
    PLAYING = 0
    DRAW = 1
    CROSS_WON = 2
    NOUGHT_WON = 3


class Mark(Enum):
    CROSS = 'x'
    NOUGHT = 'o'
    BLANK = None


class Board:
    rays = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6))

    def __init__(self, grid=None, playing=Mark.NOUGHT, status=Status.PLAYING):
        self.grid = grid or [Mark.BLANK] * 9
        self.playing = playing
        self.status = status
        self.__is_tic_tac_toe = False

    def __str__(self):
        marks = [m.value if m.value else ' ' for m in self.grid]
        rows = []
        for ray in ((6, 7, 8), (3, 4, 5), (0, 1, 2)):
            rows.append('|'.join(marks[r] for r in ray))
        grid = '\n-----\n'.join(rows)
        grid += f'\nPlaying: {self.playing.name}'
        grid += f'\nStatus: {self.status.name}'
        return grid

    def place_mark(self, square):
        if not self._is_still_on_play():
            raise GameOverException()

        if self.grid[square] != Mark.BLANK:
            raise NonBlankSquareException(square)

        self.grid[square] = self.playing
        self._update_status()
        if self._is_still_on_play():
            self._shift_turns()

    @property
    def is_still_on_play(self):
        return self._is_still_on_play()

    @property
    def is_tic_tac_toe(self):
        return self._is_tic_tac_toe()

    @property
    def is_a_draw(self):
        return self._is_a_draw()

    @property
    def available_squares(self):
        return (i for i, v in enumerate(self.grid) if v == Mark.BLANK)

    def _is_a_draw(self):
        at_least_one_blank = any(m == Mark.BLANK for m in self.grid)
        it_is = not at_least_one_blank and self.is_still_on_play
        return it_is

    def _is_tic_tac_toe(self):
        if not self.__is_tic_tac_toe:
            for ray in self.rays:
                is_tic_tac_toe = all(self.grid[r] == self.playing for r in ray)
                if is_tic_tac_toe:
                    self.__is_tic_tac_toe = True
                    break
        return self.__is_tic_tac_toe

    def _shift_turns(self):
        if self._is_still_on_play():
            self.playing = Mark.CROSS if self.playing == Mark.NOUGHT else Mark.NOUGHT

    def _update_status(self):
        if self._is_tic_tac_toe():
            self.status = Status.CROSS_WON if self.playing == Mark.CROSS else Status.NOUGHT_WON
        elif self._is_a_draw():
            self.status = Status.DRAW
        else:
            self.status = Status.PLAYING

    def _is_still_on_play(self):
        return self.status == Status.PLAYING
