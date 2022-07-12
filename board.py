from enum import Enum
from typing import Tuple, List

import numpy as np


class Player(Enum):
    NO_PLAYER = 0
    PLAYER_1 = 1
    PLAYER_2 = 2

    def player_to_symbol(self):
        if self.value == Player.NO_PLAYER.value:
            return ' '

        if self.value == Player.PLAYER_1.value:
            return 'x'

        if self.value == Player.PLAYER_2.value:
            return 'o'


class Board:

    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)

    def set_value(self, x: int, y: int, p: Player):
        assert p != Player.NO_PLAYER
        self.board[y][x] = p.value

    def get_value(self, x: int, y: int) -> Player:
        assert x < 3
        assert y < 3
        return Player(self.board[y][x])

    def board_string(self) -> str:
        return '\n'.join(['|'.join([self.get_value(x, y).player_to_symbol() for x in range(3)]) for y in range(3)])

    def get_valid_turns(self) -> List[Tuple[int, int]]:
        return [(x, y) for x in range(3) for y in range(3) if self.get_value(x, y) == Player.NO_PLAYER]

    def get_winner(self) -> Player:

        for player in [Player.PLAYER_1, Player.PLAYER_2]:
            for i in range(3):

                # Row win
                if all([self.board[i][j] == player.value for j in range(3)]):
                    return player

                # Col win
                if all([self.board[j][i] == player.value for j in range(3)]):
                    return player

            # Diag win
            if all(np.diag(self.board) == player.value):
                return player

            if all(np.diag(np.fliplr(self.board)) == player.value):
                return player

        return Player.NO_PLAYER

