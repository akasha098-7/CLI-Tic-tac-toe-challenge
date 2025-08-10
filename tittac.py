#!/usr/bin/env python3
"""
Command-line Tic-Tac-Toe with an unbeatable Minimax AI (alpha-beta pruning).

Usage:
    python tictactoe_minimax.py
"""
from functools import lru_cache

# Board positions are 0..8
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),    # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),    # cols
    (0, 4, 8), (2, 4, 6)                # diags
]

def display(board):
    chars = [c if c != '' else ' ' for c in board]
    print()
    print(f" {chars[0]} | {chars[1]} | {chars[2]} ")
    print("---+---+---")
    print(f" {chars[3]} | {chars[4]} | {chars[5]} ")
    print("---+---+---")
    print(f" {chars[6]} | {chars[7]} | {chars[8]} ")
    print()

def check_winner(board):
    for a, b, c in WINNING_LINES:
        if board[a] != '' and board[a] == board[b] == board[c]:
            return board[a]
    if '' not in board:
        return 'Draw'
    return None

def available_moves(board):
    return [i for i, v in enumerate(board) if v == '']

# We'll use caching to avoid recomputing positions
@lru_cache(maxsize=None)
def minimax_cached(board_key, ai_player, human_player, maximizing, alpha, beta):
    board = list(board_key)
    result = check_winner(board)
    if result == ai_player:
        return 1, None
    elif result == human_player:
        return -1, None
    elif result == 'Draw':
        return 0, None

    best_move = None
    if maximizing:
        value = -999
        for m in available_moves(board):
            board[m] = ai_player
            score, _ = minimax_cached(tuple(board), ai_player, human_player, False, alpha, beta)
            board[m] = ''
            if score > value:
                value = score
                best_move = m
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move
    else:
        value = 999
        for m in available_moves(board):
            board[m] = human_player
            score, _ = minimax_cached(tuple(board), ai_player, human_player, True, alpha, beta)
            board[m] = ''
            if score < value:
                value = score
                best_move = m
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_move

def ai_move(board, ai_player, human_player):
    score, move = minimax_cached(tuple(board), ai_player, human_player, True, -999, 999)
    return move

def human_move(board):
    moves = available_moves(board)
    while True:
        try:
            choice = input(
                "Enter your move (1-9), positions:\n"
                "1 2 3\n4 5 6\n7 8 9\n> "
            ).strip()
            if choice.lower() in ('q', 'quit', 'exit'):
                print("Goodbye.")
                exit(0)
            pos = int(choice) - 1
            if pos not in moves:
                print("Invalid move or already taken. Try again.")
            else:
                return pos
        except ValueError:
            print("Please enter a number 1-9.")

def play():
    print("Welcome to Tic-Tac-Toe (Unbeatable AI)\n")
    # Choose marks
    while True:
        human = input("Choose your mark (X/O) [X]: ").strip().upper()
        if human == '':
            human = 'X'
        if human in ('X', 'O'):
            break
        print("Enter X or O.")
    ai = 'O' if human == 'X' else 'X'

    # Who starts?
    while True:
        first = input("Who starts? (me/ai) [me]: ").strip().lower()
        if first == '':
            first = 'me'
        if first in ('me', 'ai'):
            break
        print("Enter 'me' or 'ai'.")

    board = [''] * 9
    current = 'human' if first == 'me' else 'ai'
    display(board)

    # Clear minimax cache (new game)
    minimax_cached.cache_clear()

    while True:
        result = check_winner(board)
        if result is not None:
            if result == 'Draw':
                print("It's a draw!")
            else:
                print(f"{result} wins!")
            display(board)
            break

        if current == 'human':
            print("Your turn.")
            m = human_move(board)
            board[m] = human
            current = 'ai'
        else:
            print("AI thinking...")
            m = ai_move(board, ai, human)
            if m is None:  # fallback (shouldn't happen)
                m = available_moves(board)[0]
            board[m] = ai
            print(f"AI played at position {m+1}.")
            current = 'human'
        display(board)

    again = input("Play again? (y/n) [y]: ").strip().lower()
    if again in ('', 'y', 'yes'):
        play()
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    play()
