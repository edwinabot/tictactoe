import unittest

from minimax import minimize, maximize
from board_representation import Board, Mark


class TestMinimize(unittest.TestCase):
    def setUp(self):
        # o|o|
        # -----
        # o| |
        # -----
        # x|x|
        self.board = Board([
            Mark.CROSS, Mark.CROSS, Mark.BLANK, Mark.NOUGHT, Mark.BLANK,
            Mark.BLANK, Mark.NOUGHT, Mark.NOUGHT, Mark.BLANK
        ],
                           playing=Mark.CROSS)

    def test_winning_move(self):
        self.board.place_mark(2)
        score = minimize(self.board, -1)
        self.assertEqual(score, -10)

    def test_loosing_move(self):
        self.board.place_mark(5)
        score = maximize(self.board, -1)
        self.assertEqual(score, 10)


if __name__ == "__main__":
    unittest.main()