from typing import Tuple

from agent import get_agent_move, get_other_player
from board import Board, Player


def main():
    print('Welcome to Tic-Pruned-Toe by BUCKFAE')

    is_p1_human = input(f'Is player 1 a human? [y/N]: ').lower() == 'y'
    is_p2_human = input(f'Is player 2 a human? [y/N]: ').lower() == 'y'

    board = Board()
    player = Player.PLAYER_1

    while True:

        # Getting next move
        if player == player.PLAYER_1:
            next_turn = get_human_move(board) if is_p1_human else get_agent_move(board, Player.PLAYER_1)
        else:
            next_turn = get_human_move(board) if is_p2_human else get_agent_move(board, Player.PLAYER_2)

        print(f'Move: {next_turn}')

        board.set_value(next_turn[0], next_turn[1], player)
        print(f'Board:\n{board.board_string()}')

        winner = board.get_winner()
        if winner != Player.NO_PLAYER or len(board.get_valid_turns()) == 0:
            print(f'\n\n{board.board_string()}\n\nWinner: {winner}')
            break

        player = get_other_player(player)


def get_human_move(board: Board) -> Tuple[int, int]:
    print(f'Your turn! Current Board:\n{board.board_string()}')
    res = [int(pos) for pos in input(f'Input: ').split(' ')]
    assert len(res) == 2
    return res[0], res[1]


if __name__ == '__main__':
    main()
