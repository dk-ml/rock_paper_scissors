from collections import Counter
from enum import Enum


class Move(Enum):
    PAPER = 'PAPER'
    ROCK = 'ROCK'
    SCISSORS = 'SCISSORS'


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.history = []
        self.winners = []

    def play(self, n_rounds=1):
        for _ in range(n_rounds):
            self._inform_players()
            round_ = Round(self.player1, self.player2)
            round_.play()
            self.history.append(round_.get_moves())
            self.winners.append(round_.get_winner())

    def _inform_players(self):
        self.player1.update(game_history=self.history)
        self.player2.update(game_history=[(b, a) for a, b in self.history])

    def get_game_stats(self):
        return Counter(self.winners)


class Round:
    WINNER_BY_MOVE = {
        (Move.PAPER, Move.PAPER): None,
        (Move.PAPER, Move.ROCK): 0,
        (Move.PAPER, Move.SCISSORS): 1,
        (Move.ROCK, Move.PAPER): 1,
        (Move.ROCK, Move.ROCK): None,
        (Move.ROCK, Move.SCISSORS): 0,
        (Move.SCISSORS, Move.PAPER): 0,
        (Move.SCISSORS, Move.ROCK): 1,
        (Move.SCISSORS, Move.SCISSORS): None,
    }

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.player1_move = None
        self.player2_move = None

    def play(self):
        self.player1_move = self.player1.get_move()
        self.player2_move = self.player2.get_move()

    def get_winner(self):
        winner = self.WINNER_BY_MOVE[self.get_moves()]
        if winner is None:
            return None
        if winner == 0:
            return self.player1
        return self.player2

    def get_moves(self):
        return (self.player1_move, self.player2_move)
