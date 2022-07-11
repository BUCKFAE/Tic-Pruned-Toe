from __future__ import annotations

import unittest

import numpy as np

from board import Board, Player


class TestBoard(unittest.TestCase):

    def test_get_winner(self):
        board = Board()

        board.board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=int)
        board.current_player = Player.PLAYER_1
        assert board.get_winner() == Player.NO_PLAYER

        board.board = np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]], dtype=int)
        board.current_player = Player.PLAYER_1
        assert board.get_winner() == Player.PLAYER_1

        board.board = np.array([[0, 0, 0], [0, 0, 0], [2, 2, 2]], dtype=int)
        board.current_player = Player.PLAYER_2
        assert board.get_winner() == Player.PLAYER_2

        board.board = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]], dtype=int)
        board.current_player = Player.PLAYER_1
        assert board.get_winner() == Player.PLAYER_1

        board.board = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=int)
        board.current_player = Player.PLAYER_1
        assert board.get_winner() == Player.PLAYER_1

        board.board = np.array([[0, 0, 2], [0, 2, 0], [2, 0, 0]], dtype=int)
        board.current_player = Player.PLAYER_2
        assert board.get_winner() == Player.PLAYER_2

    def test_get_next_player(self):
        board = Board()
        assert board.get_next_player() == Player.PLAYER_1
        assert board.get_next_player() == Player.PLAYER_2
        assert board.get_next_player() == Player.PLAYER_1
        assert board.get_next_player() == Player.PLAYER_2
        assert board.get_next_player() == Player.PLAYER_1
        assert board.get_next_player() == Player.PLAYER_2


if __name__ == '__main__':
    unittest.main()
