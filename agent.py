import random
import sys
from math import inf
from typing import Tuple, List, Optional

import numpy as np

from board import Board, Player


class Node:

    def __init__(self, board: Board, is_max: bool, own_player: Player, path: Optional[Tuple[int, int]]=None):
        """Board is a fresh copy"""
        self._board = board
        self._own_player = own_player
        self.is_max = is_max
        self.path = path

    def is_leaf(self) -> bool:
        return len(self._board.get_valid_turns()) == 0 or self._board.get_winner() != Player.NO_PLAYER

    def get_value(self) -> int:
        winner = self._board.get_winner()

        # Player 1 won
        if winner == Player.PLAYER_1:
            return 1 if self._own_player == Player.PLAYER_1 else - 1

        # Player 2 won
        if winner == Player.PLAYER_2:
            return 1 if self._own_player == Player.PLAYER_2 else - 1

        # No player won / game still in progress
        return 0

    def get_children(self) -> List['Node']:
        children = []

        if self.is_max:
            player = Player(self._own_player.value)
        else:
            player = get_other_player(self._own_player)

        for turn in self._board.get_valid_turns():
            new_board = copy_board(self._board)
            new_board.set_value(turn[0], turn[1], player)
            children.append(Node(new_board, not self.is_max, self._own_player, (turn[0], turn[1])))

        random.shuffle(children)
        return children


def get_agent_move(board: Board, own_player: Player) -> Tuple[int, int]:
    root = Node(copy_board(board), True, own_player)
    value, path = minmax(root, -5, +5, True)
    print(f'Player: {own_player} Value: {value} - Path: {path}')
    return path


def minmax(node, alpha, beta, is_max):
    if node.is_leaf():
        #print(f'Node: {node.get_value()} - {node._own_player}')
        #print(node._board.board_string())
        #print("-" * 10)

        return node.get_value(), node.path

    if is_max:
        value = -5
        best_move = None

        for child in node.get_children()[::-1]:

            res, path = minmax(child, alpha, beta, False)

            if res >= value:
                value = res
                best_move = child.path

            if value >= beta:
                break
                pass
            #    break
            alpha = max(alpha, value)
        return value, best_move

    else:
        value = +5
        best_move = None
        for child in node.get_children():

            res, path = minmax(child, alpha, beta, True)

            if res <= value:
                value = res
                best_move = child.path

            if value <= alpha:
                pass
                #break
            beta = min(beta, value)
        return value, best_move


def get_other_player(player: Player) -> Player:
    if player == player.PLAYER_2 or player == player.NO_PLAYER:
        return Player.PLAYER_1
    return Player.PLAYER_2


def copy_board(board: Board) -> Board:
    b = Board()
    b.board = np.copy(board.board)
    return b
