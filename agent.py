import random
import sys
from math import inf
from typing import Tuple, List

import numpy as np

from board import Board, Player

c = 0


class Node:

    def __init__(self, board: Board, is_max: bool, own_player: Player, path=None):
        self._board = board
        self._possible_moves = board.get_valid_turns()
        self._value = None
        self._children = None
        self._own_player = own_player
        self.is_max = is_max
        self.path = path

    def is_leaf(self) -> bool:
        return len(self._possible_moves) == 0 or self._board.get_winner() != Player.NO_PLAYER

    def get_value(self) -> float:
        if self._value is None:
            winner = self._board.get_winner()
            if winner == Player.PLAYER_1:
                self._value = 1 if self._own_player == Player.PLAYER_1 else - 1
            elif winner == Player.PLAYER_2:
                self._value = 1 if self._own_player == Player.PLAYER_2 else - 1
            else:
                self._value = 0
        return self._value

    def get_children(self) -> List['Node']:
        global c
        if self._children is None:
            self._children = []
            current_player = self._board.current_player
            next_player = self._board.get_next_player()
            #print(f'Existing:\n{self._board.board_string()}')
            for turn in self._possible_moves:
                #print(f'Turn: {turn}')
                new_board = copy_board(self._board)
                new_board.current_player = next_player
                new_board.set_value(turn[0], turn[1], current_player)
                #print(f'New:\n{new_board.board_string()}')
                self._children.append(Node(new_board, not self.is_max, self._own_player, (turn[0], turn[1])))

        if self.is_leaf():
            c += 1
            #print("-" * 10)
            #print(f'Board:\n{self._board.board_string()}')
            #print(f'Value: {self.get_value()}')
            #if c <= 3:
                #sys.exit(0)
        return self._children


def get_agent_move(board: Board, own_player: Player) -> Tuple[int, int]:
    root = Node(copy_board(board), True, own_player)
    value, path = minmax(root, -inf, +inf, True)
    print(f'Player: {own_player} Value: {value} - Path: {path}')
    return path

def minmax(node, alpha, beta, is_max):
    if node.is_leaf():
        return node.get_value(), node.path

    if is_max:
        value = -inf
        best_move = None

        for child in node.get_children():

            res, path = minmax(child, alpha, beta, False)

            if res >= value:
                value = res
                best_move = child.path

            if value >= beta:
                break
            alpha = max(alpha, value)
        return value, best_move

    else:
        value = +inf
        best_move = None
        for child in node.get_children():

            res, path = minmax(child, alpha, beta, True)

            if res <= value:
                value = res
                best_move = child.path

            if value <= alpha:
                break
            beta = min(beta, value)
        return value, best_move


def get_other_player(player: Player) -> Player:
    if player == player.PLAYER_2 or player.NO_PLAYER:
        return Player.PLAYER_1
    return Player.PLAYER_2


def copy_board(board: Board) -> Board:
    b = Board()
    b.board = np.copy(board.board)
    b.current_player = Player(board.current_player.value)
    return b
