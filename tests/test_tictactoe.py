import unittest

from tictactoe import ai_play
from board_representation import Board, Mark


class TestAIPlay(unittest.TestCase):
    def test_ai_winning(self):
        board = Board([
            Mark.CROSS, Mark.CROSS, Mark.BLANK, Mark.NOUGHT, Mark.BLANK,
            Mark.BLANK, Mark.NOUGHT, Mark.NOUGHT, Mark.BLANK
        ],
                      playing=Mark.CROSS)
        ai_play(board)

        # o|o|
        # -----
        # o| |
        # -----
        # x|x|
        self.assertTrue(board.is_tic_tac_toe)
        self.assertEqual(board.playing, Mark.CROSS)

    def test_avoid_loosing(self):
        #  | |
        # -----
        # o| |o
        # -----
        # x| |
        board = Board([
            Mark.CROSS, Mark.BLANK, Mark.BLANK, Mark.NOUGHT, Mark.BLANK,
            Mark.NOUGHT, Mark.BLANK, Mark.BLANK, Mark.BLANK
        ],
                      playing=Mark.CROSS)
        ai_play(board)
        self.assertEqual(board.grid[4], Mark.CROSS)

    def test_ai_winning_2(self):
        # o| |
        # -----
        # x|x|
        # -----
        # o| |
        board = Board([
            Mark.NOUGHT, Mark.BLANK, Mark.BLANK, Mark.CROSS, Mark.CROSS,
            Mark.BLANK, Mark.NOUGHT, Mark.BLANK, Mark.BLANK
        ],
                      playing=Mark.CROSS)
        ai_play(board)
        self.assertTrue(board.is_tic_tac_toe)
        self.assertEqual(board.grid[5], Mark.CROSS)


if __name__ == "__main__":
    # unittest.main(argv=['.', 'TestAIPlay.test_ai_winning_2'])
    unittest.main()
